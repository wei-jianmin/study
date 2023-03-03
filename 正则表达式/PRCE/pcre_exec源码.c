/*************************************************
*         Execute a Regular Expression           *
*************************************************/

/* This function applies a compiled re to a subject string and picks out
portions of the string if it matches. Two elements in the vector are set for
each substring: the offsets to the start and end of the substring.

Arguments:
  argument_re     points to the compiled expression
  extra_data      points to extra data or is NULL
  subject         points to the subject string
  length          length of subject string (may contain binary zeros)
  start_offset    where to start in the subject string
  options         option bits
  offsets         points to a vector of ints to be filled in with offsets
  offsetcount     the number of elements in the vector

Returns:          > 0 => success; value is the number of elements filled in
                  = 0 => success, but offsets is not big enough
                   -1 => failed to match
                 < -1 => some kind of unexpected problem
*/

#if defined COMPILE_PCRE8
PCRE_EXP_DEFN int PCRE_CALL_CONVENTION
pcre_exec(const pcre *argument_re, const pcre_extra *extra_data,
  PCRE_SPTR subject, int length, int start_offset, int options, int *offsets,
  int offsetcount)
#elif defined COMPILE_PCRE16
PCRE_EXP_DEFN int PCRE_CALL_CONVENTION
pcre16_exec(const pcre16 *argument_re, const pcre16_extra *extra_data,
  PCRE_SPTR16 subject, int length, int start_offset, int options, int *offsets,
  int offsetcount)
#elif defined COMPILE_PCRE32
PCRE_EXP_DEFN int PCRE_CALL_CONVENTION
pcre32_exec(const pcre32 *argument_re, const pcre32_extra *extra_data,
  PCRE_SPTR32 subject, int length, int start_offset, int options, int *offsets,
  int offsetcount)
#endif
{
int rc, ocount, arg_offset_max;
int newline;
BOOL using_temporary_offsets = FALSE;
BOOL anchored;
BOOL startline;
BOOL firstline;
BOOL utf;
BOOL has_first_char = FALSE;
BOOL has_req_char = FALSE;
pcre_uchar first_char = 0;
pcre_uchar first_char2 = 0;
pcre_uchar req_char = 0;
pcre_uchar req_char2 = 0;
match_data match_block;
match_data *md = &match_block;
const pcre_uint8 *tables;
const pcre_uint8 *start_bits = NULL;
PCRE_PUCHAR start_match = (PCRE_PUCHAR)subject + start_offset;
PCRE_PUCHAR end_subject;
PCRE_PUCHAR start_partial = NULL;
PCRE_PUCHAR match_partial = NULL;
PCRE_PUCHAR req_char_ptr = start_match - 1;

const pcre_study_data *study;
const REAL_PCRE *re = (const REAL_PCRE *)argument_re;

#ifdef NO_RECURSE
heapframe frame_zero;
frame_zero.Xprevframe = NULL;            /* Marks the top level */
frame_zero.Xnextframe = NULL;            /* None are allocated yet */
md->match_frames_base = &frame_zero;
#endif

/* Check for the special magic call that measures the size of the stack used
per recursive call of match(). Without the funny casting for sizeof, a Windows
compiler gave this error: "unary minus operator applied to unsigned type,
result still unsigned". Hopefully the cast fixes that. */

if (re == NULL && extra_data == NULL && subject == NULL && length == -999 &&
    start_offset == -999)
#ifdef NO_RECURSE
  return -((int)sizeof(heapframe));
#else
  return match(NULL, NULL, NULL, 0, NULL, NULL, 0);
#endif

/* Plausibility checks */

if ((options & ~PUBLIC_EXEC_OPTIONS) != 0) return PCRE_ERROR_BADOPTION;
if (re == NULL || subject == NULL || (offsets == NULL && offsetcount > 0))
  return PCRE_ERROR_NULL;
if (offsetcount < 0) return PCRE_ERROR_BADCOUNT;
if (length < 0) return PCRE_ERROR_BADLENGTH;
if (start_offset < 0 || start_offset > length) return PCRE_ERROR_BADOFFSET;

/* Check that the first field in the block is the magic number. If it is not,
return with PCRE_ERROR_BADMAGIC. However, if the magic number is equal to
REVERSED_MAGIC_NUMBER we return with PCRE_ERROR_BADENDIANNESS, which
means that the pattern is likely compiled with different endianness. */

if (re->magic_number != MAGIC_NUMBER)
  return re->magic_number == REVERSED_MAGIC_NUMBER?
    PCRE_ERROR_BADENDIANNESS:PCRE_ERROR_BADMAGIC;
if ((re->flags & PCRE_MODE) == 0) return PCRE_ERROR_BADMODE;

/* These two settings are used in the code for checking a UTF-8 string that
follows immediately afterwards. Other values in the md block are used only
during "normal" pcre_exec() processing, not when the JIT support is in use,
so they are set up later. */

/* PCRE_UTF16 has the same value as PCRE_UTF8. */
utf = md->utf = (re->options & PCRE_UTF8) != 0;
md->partial = ((options & PCRE_PARTIAL_HARD) != 0)? 2 :
              ((options & PCRE_PARTIAL_SOFT) != 0)? 1 : 0;

/* Check a UTF-8 string if required. Pass back the character offset and error
code for an invalid string if a results vector is available. */

#ifdef SUPPORT_UTF
if (utf && (options & PCRE_NO_UTF8_CHECK) == 0)
  {
  int erroroffset;
  int errorcode = PRIV(valid_utf)((PCRE_PUCHAR)subject, length, &erroroffset);
  if (errorcode != 0)
    {
    if (offsetcount >= 2)
      {
      offsets[0] = erroroffset;
      offsets[1] = errorcode;
      }
#if defined COMPILE_PCRE8
    return (errorcode <= PCRE_UTF8_ERR5 && md->partial > 1)?
      PCRE_ERROR_SHORTUTF8 : PCRE_ERROR_BADUTF8;
#elif defined COMPILE_PCRE16
    return (errorcode <= PCRE_UTF16_ERR1 && md->partial > 1)?
      PCRE_ERROR_SHORTUTF16 : PCRE_ERROR_BADUTF16;
#elif defined COMPILE_PCRE32
    return PCRE_ERROR_BADUTF32;
#endif
    }
#if defined COMPILE_PCRE8 || defined COMPILE_PCRE16
  /* Check that a start_offset points to the start of a UTF character. */
  if (start_offset > 0 && start_offset < length &&
      NOT_FIRSTCHAR(((PCRE_PUCHAR)subject)[start_offset]))
    return PCRE_ERROR_BADUTF8_OFFSET;
#endif
  }
#endif

/* If the pattern was successfully studied with JIT support, run the JIT
executable instead of the rest of this function. Most options must be set at
compile time for the JIT code to be usable. Fallback to the normal code path if
an unsupported flag is set. */

#ifdef SUPPORT_JIT
if (extra_data != NULL
    && (extra_data->flags & (PCRE_EXTRA_EXECUTABLE_JIT |
                             PCRE_EXTRA_TABLES)) == PCRE_EXTRA_EXECUTABLE_JIT
    && extra_data->executable_jit != NULL
    && (options & ~PUBLIC_JIT_EXEC_OPTIONS) == 0)
  {
  rc = PRIV(jit_exec)(extra_data, (const pcre_uchar *)subject, length,
       start_offset, options, offsets, offsetcount);

  /* PCRE_ERROR_NULL means that the selected normal or partial matching
  mode is not compiled. In this case we simply fallback to interpreter. */

  if (rc != PCRE_ERROR_JIT_BADOPTION) return rc;
  }
#endif

/* Carry on with non-JIT matching. This information is for finding all the
numbers associated with a given name, for condition testing. */

md->name_table = (pcre_uchar *)re + re->name_table_offset;
md->name_count = re->name_count;
md->name_entry_size = re->name_entry_size;

/* Fish out the optional data from the extra_data structure, first setting
the default values. */

study = NULL;
md->match_limit = MATCH_LIMIT;
md->match_limit_recursion = MATCH_LIMIT_RECURSION;
md->callout_data = NULL;

/* The table pointer is always in native byte order. */

tables = re->tables;

/* The two limit values override the defaults, whatever their value. */

if (extra_data != NULL)
  {
  unsigned long int flags = extra_data->flags;
  if ((flags & PCRE_EXTRA_STUDY_DATA) != 0)
    study = (const pcre_study_data *)extra_data->study_data;
  if ((flags & PCRE_EXTRA_MATCH_LIMIT) != 0)
    md->match_limit = extra_data->match_limit;
  if ((flags & PCRE_EXTRA_MATCH_LIMIT_RECURSION) != 0)
    md->match_limit_recursion = extra_data->match_limit_recursion;
  if ((flags & PCRE_EXTRA_CALLOUT_DATA) != 0)
    md->callout_data = extra_data->callout_data;
  if ((flags & PCRE_EXTRA_TABLES) != 0) tables = extra_data->tables;
  }

/* Limits in the regex override only if they are smaller. */

if ((re->flags & PCRE_MLSET) != 0 && re->limit_match < md->match_limit)
  md->match_limit = re->limit_match;

if ((re->flags & PCRE_RLSET) != 0 &&
    re->limit_recursion < md->match_limit_recursion)
  md->match_limit_recursion = re->limit_recursion;

/* If the exec call supplied NULL for tables, use the inbuilt ones. This
is a feature that makes it possible to save compiled regex and re-use them
in other programs later. */

if (tables == NULL) tables = PRIV(default_tables);

/* Set up other data */

anchored = ((re->options | options) & PCRE_ANCHORED) != 0;
startline = (re->flags & PCRE_STARTLINE) != 0;
firstline = (re->options & PCRE_FIRSTLINE) != 0;

/* The code starts after the real_pcre block and the capture name table. */

md->start_code = (const pcre_uchar *)re + re->name_table_offset +
  re->name_count * re->name_entry_size;

md->start_subject = (PCRE_PUCHAR)subject;
md->start_offset = start_offset;
md->end_subject = md->start_subject + length;
end_subject = md->end_subject;

md->endonly = (re->options & PCRE_DOLLAR_ENDONLY) != 0;
md->use_ucp = (re->options & PCRE_UCP) != 0;
md->jscript_compat = (re->options & PCRE_JAVASCRIPT_COMPAT) != 0;
md->ignore_skip_arg = 0;

/* Some options are unpacked into BOOL variables in the hope that testing
them will be faster than individual option bits. */

md->notbol = (options & PCRE_NOTBOL) != 0;
md->noteol = (options & PCRE_NOTEOL) != 0;
md->notempty = (options & PCRE_NOTEMPTY) != 0;
md->notempty_atstart = (options & PCRE_NOTEMPTY_ATSTART) != 0;

md->hitend = FALSE;
md->mark = md->nomatch_mark = NULL;     /* In case never set */

md->recursive = NULL;                   /* No recursion at top level */
md->hasthen = (re->flags & PCRE_HASTHEN) != 0;

md->lcc = tables + lcc_offset;
md->fcc = tables + fcc_offset;
md->ctypes = tables + ctypes_offset;

/* Handle different \R options. */

switch (options & (PCRE_BSR_ANYCRLF|PCRE_BSR_UNICODE))
  {
  case 0:
  if ((re->options & (PCRE_BSR_ANYCRLF|PCRE_BSR_UNICODE)) != 0)
    md->bsr_anycrlf = (re->options & PCRE_BSR_ANYCRLF) != 0;
  else
#ifdef BSR_ANYCRLF
  md->bsr_anycrlf = TRUE;
#else
  md->bsr_anycrlf = FALSE;
#endif
  break;

  case PCRE_BSR_ANYCRLF:
  md->bsr_anycrlf = TRUE;
  break;

  case PCRE_BSR_UNICODE:
  md->bsr_anycrlf = FALSE;
  break;

  default: return PCRE_ERROR_BADNEWLINE;
  }

/* Handle different types of newline. The three bits give eight cases. If
nothing is set at run time, whatever was used at compile time applies. */

switch ((((options & PCRE_NEWLINE_BITS) == 0)? re->options :
        (pcre_uint32)options) & PCRE_NEWLINE_BITS)
  {
  case 0: newline = NEWLINE; break;   /* Compile-time default */
  case PCRE_NEWLINE_CR: newline = CHAR_CR; break;
  case PCRE_NEWLINE_LF: newline = CHAR_NL; break;
  case PCRE_NEWLINE_CR+
       PCRE_NEWLINE_LF: newline = (CHAR_CR << 8) | CHAR_NL; break;
  case PCRE_NEWLINE_ANY: newline = -1; break;
  case PCRE_NEWLINE_ANYCRLF: newline = -2; break;
  default: return PCRE_ERROR_BADNEWLINE;
  }

if (newline == -2)
  {
  md->nltype = NLTYPE_ANYCRLF;
  }
else if (newline < 0)
  {
  md->nltype = NLTYPE_ANY;
  }
else
  {
  md->nltype = NLTYPE_FIXED;
  if (newline > 255)
    {
    md->nllen = 2;
    md->nl[0] = (newline >> 8) & 255;
    md->nl[1] = newline & 255;
    }
  else
    {
    md->nllen = 1;
    md->nl[0] = newline;
    }
  }

/* Partial matching was originally supported only for a restricted set of
regexes; from release 8.00 there are no restrictions, but the bits are still
defined (though never set). So there's no harm in leaving this code. */

if (md->partial && (re->flags & PCRE_NOPARTIAL) != 0)
  return PCRE_ERROR_BADPARTIAL;

/* If the expression has got more back references than the offsets supplied can
hold, we get a temporary chunk of working store to use during the matching.
Otherwise, we can use the vector supplied, rounding down its size to a multiple
of 3. */

ocount = offsetcount - (offsetcount % 3);
arg_offset_max = (2*ocount)/3;

if (re->top_backref > 0 && re->top_backref >= ocount/3)
  {
  ocount = re->top_backref * 3 + 3;
  md->offset_vector = (int *)(PUBL(malloc))(ocount * sizeof(int));
  if (md->offset_vector == NULL) return PCRE_ERROR_NOMEMORY;
  using_temporary_offsets = TRUE;
  DPRINTF(("Got memory to hold back references\n"));
  }
else md->offset_vector = offsets;
md->offset_end = ocount;
md->offset_max = (2*ocount)/3;
md->capture_last = 0;

/* Reset the working variable associated with each extraction. These should
never be used unless previously set, but they get saved and restored, and so we
initialize them to avoid reading uninitialized locations. Also, unset the
offsets for the matched string. This is really just for tidiness with callouts,
in case they inspect these fields. */

if (md->offset_vector != NULL)
  {
  register int *iptr = md->offset_vector + ocount;
  register int *iend = iptr - re->top_bracket;
  if (iend < md->offset_vector + 2) iend = md->offset_vector + 2;
  while (--iptr >= iend) *iptr = -1;
  if (offsetcount > 0) md->offset_vector[0] = -1;
  if (offsetcount > 1) md->offset_vector[1] = -1;
  }

/* Set up the first character to match, if available. The first_char value is
never set for an anchored regular expression, but the anchoring may be forced
at run time, so we have to test for anchoring. The first char may be unset for
an unanchored pattern, of course. If there's no first char and the pattern was
studied, there may be a bitmap of possible first characters. */

if (!anchored)
  {
  if ((re->flags & PCRE_FIRSTSET) != 0)
    {
    has_first_char = TRUE;
    first_char = first_char2 = (pcre_uchar)(re->first_char);
    if ((re->flags & PCRE_FCH_CASELESS) != 0)
      {
      first_char2 = TABLE_GET(first_char, md->fcc, first_char);
#if defined SUPPORT_UCP && !(defined COMPILE_PCRE8)
      if (utf && first_char > 127)
        first_char2 = UCD_OTHERCASE(first_char);
#endif
      }
    }
  else
    if (!startline && study != NULL &&
      (study->flags & PCRE_STUDY_MAPPED) != 0)
        start_bits = study->start_bits;
  }

/* For anchored or unanchored matches, there may be a "last known required
character" set. */

if ((re->flags & PCRE_REQCHSET) != 0)
  {
  has_req_char = TRUE;
  req_char = req_char2 = (pcre_uchar)(re->req_char);
  if ((re->flags & PCRE_RCH_CASELESS) != 0)
    {
    req_char2 = TABLE_GET(req_char, md->fcc, req_char);
#if defined SUPPORT_UCP && !(defined COMPILE_PCRE8)
    if (utf && req_char > 127)
      req_char2 = UCD_OTHERCASE(req_char);
#endif
    }
  }


/* ==========================================================================*/

/* Loop for handling unanchored repeated matching attempts; for anchored regexs
the loop runs just once. */

for(;;)
  {
  PCRE_PUCHAR save_end_subject = end_subject;
  PCRE_PUCHAR new_start_match;

  /* If firstline is TRUE, the start of the match is constrained to the first
  line of a multiline string. That is, the match must be before or at the first
  newline. Implement this by temporarily adjusting end_subject so that we stop
  scanning at a newline. If the match fails at the newline, later code breaks
  this loop. */

  if (firstline)
    {
    PCRE_PUCHAR t = start_match;
#ifdef SUPPORT_UTF
    if (utf)
      {
      while (t < md->end_subject && !IS_NEWLINE(t))
        {
        t++;
        ACROSSCHAR(t < end_subject, *t, t++);
        }
      }
    else
#endif
    while (t < md->end_subject && !IS_NEWLINE(t)) t++;
    end_subject = t;
    }

  /* There are some optimizations that avoid running the match if a known
  starting point is not found, or if a known later character is not present.
  However, there is an option that disables these, for testing and for ensuring
  that all callouts do actually occur. The option can be set in the regex by
  (*NO_START_OPT) or passed in match-time options. */

  if (((options | re->options) & PCRE_NO_START_OPTIMIZE) == 0)
    {
    /* Advance to a unique first char if there is one. */

    if (has_first_char)
      {
      pcre_uchar smc;

      if (first_char != first_char2)
        while (start_match < end_subject &&
          (smc = UCHAR21TEST(start_match)) != first_char && smc != first_char2)
          start_match++;
      else
        while (start_match < end_subject && UCHAR21TEST(start_match) != first_char)
          start_match++;
      }

    /* Or to just after a linebreak for a multiline match */

    else if (startline)
      {
      if (start_match > md->start_subject + start_offset)
        {
#ifdef SUPPORT_UTF
        if (utf)
          {
          while (start_match < end_subject && !WAS_NEWLINE(start_match))
            {
            start_match++;
            ACROSSCHAR(start_match < end_subject, *start_match,
              start_match++);
            }
          }
        else
#endif
        while (start_match < end_subject && !WAS_NEWLINE(start_match))
          start_match++;

        /* If we have just passed a CR and the newline option is ANY or ANYCRLF,
        and we are now at a LF, advance the match position by one more character.
        */

        if (start_match[-1] == CHAR_CR &&
             (md->nltype == NLTYPE_ANY || md->nltype == NLTYPE_ANYCRLF) &&
             start_match < end_subject &&
             UCHAR21TEST(start_match) == CHAR_NL)
          start_match++;
        }
      }

    /* Or to a non-unique first byte after study */

    else if (start_bits != NULL)
      {
      while (start_match < end_subject)
        {
        register pcre_uint32 c = UCHAR21TEST(start_match);
#ifndef COMPILE_PCRE8
        if (c > 255) c = 255;
#endif
        if ((start_bits[c/8] & (1 << (c&7))) != 0) break;
        start_match++;
        }
      }
    }   /* Starting optimizations */

  /* Restore fudged end_subject */

  end_subject = save_end_subject;

  /* The following two optimizations are disabled for partial matching or if
  disabling is explicitly requested. */

  if (((options | re->options) & PCRE_NO_START_OPTIMIZE) == 0 && !md->partial)
    {
    /* If the pattern was studied, a minimum subject length may be set. This is
    a lower bound; no actual string of that length may actually match the
    pattern. Although the value is, strictly, in characters, we treat it as
    bytes to avoid spending too much time in this optimization. */

    if (study != NULL && (study->flags & PCRE_STUDY_MINLEN) != 0 &&
        (pcre_uint32)(end_subject - start_match) < study->minlength)
      {
      rc = MATCH_NOMATCH;
      break;
      }

    /* If req_char is set, we know that that character must appear in the
    subject for the match to succeed. If the first character is set, req_char
    must be later in the subject; otherwise the test starts at the match point.
    This optimization can save a huge amount of backtracking in patterns with
    nested unlimited repeats that aren't going to match. Writing separate code
    for cased/caseless versions makes it go faster, as does using an
    autoincrement and backing off on a match.

    HOWEVER: when the subject string is very, very long, searching to its end
    can take a long time, and give bad performance on quite ordinary patterns.
    This showed up when somebody was matching something like /^\d+C/ on a
    32-megabyte string... so we don't do this when the string is sufficiently
    long. */

    if (has_req_char && end_subject - start_match < REQ_BYTE_MAX)
      {
      register PCRE_PUCHAR p = start_match + (has_first_char? 1:0);

      /* We don't need to repeat the search if we haven't yet reached the
      place we found it at last time. */

      if (p > req_char_ptr)
        {
        if (req_char != req_char2)
          {
          while (p < end_subject)
            {
            register pcre_uint32 pp = UCHAR21INCTEST(p);
            if (pp == req_char || pp == req_char2) { p--; break; }
            }
          }
        else
          {
          while (p < end_subject)
            {
            if (UCHAR21INCTEST(p) == req_char) { p--; break; }
            }
          }

        /* If we can't find the required character, break the matching loop,
        forcing a match failure. */

        if (p >= end_subject)
          {
          rc = MATCH_NOMATCH;
          break;
          }

        /* If we have found the required character, save the point where we
        found it, so that we don't search again next time round the loop if
        the start hasn't passed this character yet. */

        req_char_ptr = p;
        }
      }
    }

#ifdef PCRE_DEBUG  /* Sigh. Some compilers never learn. */
  printf(">>>> Match against: ");
  pchars(start_match, end_subject - start_match, TRUE, md);
  printf("\n");
#endif

  /* OK, we can now run the match. If "hitend" is set afterwards, remember the
  first starting point for which a partial match was found. */

  md->start_match_ptr = start_match;
  md->start_used_ptr = start_match;
  md->match_call_count = 0;
  md->match_function_type = 0;
  md->end_offset_top = 0;
  md->skip_arg_count = 0;
  rc = match(start_match, md->start_code, start_match, 2, md, NULL, 0);
  if (md->hitend && start_partial == NULL)
    {
    start_partial = md->start_used_ptr;
    match_partial = start_match;
    }

  switch(rc)
    {
    /* If MATCH_SKIP_ARG reaches this level it means that a MARK that matched
    the SKIP's arg was not found. In this circumstance, Perl ignores the SKIP
    entirely. The only way we can do that is to re-do the match at the same
    point, with a flag to force SKIP with an argument to be ignored. Just
    treating this case as NOMATCH does not work because it does not check other
    alternatives in patterns such as A(*SKIP:A)B|AC when the subject is AC. */

    case MATCH_SKIP_ARG:
    new_start_match = start_match;
    md->ignore_skip_arg = md->skip_arg_count;
    break;

    /* SKIP passes back the next starting point explicitly, but if it is no
    greater than the match we have just done, treat it as NOMATCH. */

    case MATCH_SKIP:
    if (md->start_match_ptr > start_match)
      {
      new_start_match = md->start_match_ptr;
      break;
      }
    /* Fall through */

    /* NOMATCH and PRUNE advance by one character. THEN at this level acts
    exactly like PRUNE. Unset ignore SKIP-with-argument. */

    case MATCH_NOMATCH:
    case MATCH_PRUNE:
    case MATCH_THEN:
    md->ignore_skip_arg = 0;
    new_start_match = start_match + 1;
#ifdef SUPPORT_UTF
    if (utf)
      ACROSSCHAR(new_start_match < end_subject, *new_start_match,
        new_start_match++);
#endif
    break;

    /* COMMIT disables the bumpalong, but otherwise behaves as NOMATCH. */

    case MATCH_COMMIT:
    rc = MATCH_NOMATCH;
    goto ENDLOOP;

    /* Any other return is either a match, or some kind of error. */

    default:
    goto ENDLOOP;
    }

  /* Control reaches here for the various types of "no match at this point"
  result. Reset the code to MATCH_NOMATCH for subsequent checking. */

  rc = MATCH_NOMATCH;

  /* If PCRE_FIRSTLINE is set, the match must happen before or at the first
  newline in the subject (though it may continue over the newline). Therefore,
  if we have just failed to match, starting at a newline, do not continue. */

  if (firstline && IS_NEWLINE(start_match)) break;

  /* Advance to new matching position */

  start_match = new_start_match;

  /* Break the loop if the pattern is anchored or if we have passed the end of
  the subject. */

  if (anchored || start_match > end_subject) break;

  /* If we have just passed a CR and we are now at a LF, and the pattern does
  not contain any explicit matches for \r or \n, and the newline option is CRLF
  or ANY or ANYCRLF, advance the match position by one more character. In
  normal matching start_match will aways be greater than the first position at
  this stage, but a failed *SKIP can cause a return at the same point, which is
  why the first test exists. */

  if (start_match > (PCRE_PUCHAR)subject + start_offset &&
      start_match[-1] == CHAR_CR &&
      start_match < end_subject &&
      *start_match == CHAR_NL &&
      (re->flags & PCRE_HASCRORLF) == 0 &&
        (md->nltype == NLTYPE_ANY ||
         md->nltype == NLTYPE_ANYCRLF ||
         md->nllen == 2))
    start_match++;

  md->mark = NULL;   /* Reset for start of next match attempt */
  }                  /* End of for(;;) "bumpalong" loop */

/* ==========================================================================*/

/* We reach here when rc is not MATCH_NOMATCH, or if one of the stopping
conditions is true:

(1) The pattern is anchored or the match was failed by (*COMMIT);

(2) We are past the end of the subject;

(3) PCRE_FIRSTLINE is set and we have failed to match at a newline, because
    this option requests that a match occur at or before the first newline in
    the subject.

When we have a match and the offset vector is big enough to deal with any
backreferences, captured substring offsets will already be set up. In the case
where we had to get some local store to hold offsets for backreference
processing, copy those that we can. In this case there need not be overflow if
certain parts of the pattern were not used, even though there are more
capturing parentheses than vector slots. */

ENDLOOP:

if (rc == MATCH_MATCH || rc == MATCH_ACCEPT)
  {
  if (using_temporary_offsets)
    {
    if (arg_offset_max >= 4)
      {
      memcpy(offsets + 2, md->offset_vector + 2,
        (arg_offset_max - 2) * sizeof(int));
      DPRINTF(("Copied offsets from temporary memory\n"));
      }
    if (md->end_offset_top > arg_offset_max) md->capture_last |= OVFLBIT;
    DPRINTF(("Freeing temporary memory\n"));
    (PUBL(free))(md->offset_vector);
    }

  /* Set the return code to the number of captured strings, or 0 if there were
  too many to fit into the vector. */

  rc = ((md->capture_last & OVFLBIT) != 0 &&
         md->end_offset_top >= arg_offset_max)?
    0 : md->end_offset_top/2;

  /* If there is space in the offset vector, set any unused pairs at the end of
  the pattern to -1 for backwards compatibility. It is documented that this
  happens. In earlier versions, the whole set of potential capturing offsets
  was set to -1 each time round the loop, but this is handled differently now.
  "Gaps" are set to -1 dynamically instead (this fixes a bug). Thus, it is only
  those at the end that need unsetting here. We can't just unset them all at
  the start of the whole thing because they may get set in one branch that is
  not the final matching branch. */

  if (md->end_offset_top/2 <= re->top_bracket && offsets != NULL)
    {
    register int *iptr, *iend;
    int resetcount = 2 + re->top_bracket * 2;
    if (resetcount > offsetcount) resetcount = offsetcount;
    iptr = offsets + md->end_offset_top;
    iend = offsets + resetcount;
    while (iptr < iend) *iptr++ = -1;
    }

  /* If there is space, set up the whole thing as substring 0. The value of
  md->start_match_ptr might be modified if \K was encountered on the success
  matching path. */

  if (offsetcount < 2) rc = 0; else
    {
    offsets[0] = (int)(md->start_match_ptr - md->start_subject);
    offsets[1] = (int)(md->end_match_ptr - md->start_subject);
    }

  /* Return MARK data if requested */

  if (extra_data != NULL && (extra_data->flags & PCRE_EXTRA_MARK) != 0)
    *(extra_data->mark) = (pcre_uchar *)md->mark;
  DPRINTF((">>>> returning %d\n", rc));
#ifdef NO_RECURSE
  release_match_heapframes(&frame_zero);
#endif
  return rc;
  }

/* Control gets here if there has been an error, or if the overall match
attempt has failed at all permitted starting positions. */

if (using_temporary_offsets)
  {
  DPRINTF(("Freeing temporary memory\n"));
  (PUBL(free))(md->offset_vector);
  }

/* For anything other than nomatch or partial match, just return the code. */

if (rc != MATCH_NOMATCH && rc != PCRE_ERROR_PARTIAL)
  {
  DPRINTF((">>>> error: returning %d\n", rc));
#ifdef NO_RECURSE
  release_match_heapframes(&frame_zero);
#endif
  return rc;
  }

/* Handle partial matches - disable any mark data */

if (match_partial != NULL)
  {
  DPRINTF((">>>> returning PCRE_ERROR_PARTIAL\n"));
  md->mark = NULL;
  if (offsetcount > 1)
    {
    offsets[0] = (int)(start_partial - (PCRE_PUCHAR)subject);
    offsets[1] = (int)(end_subject - (PCRE_PUCHAR)subject);
    if (offsetcount > 2)
      offsets[2] = (int)(match_partial - (PCRE_PUCHAR)subject);
    }
  rc = PCRE_ERROR_PARTIAL;
  }

/* This is the classic nomatch case */

else
  {
  DPRINTF((">>>> returning PCRE_ERROR_NOMATCH\n"));
  rc = PCRE_ERROR_NOMATCH;
  }

/* Return the MARK data if it has been requested. */

if (extra_data != NULL && (extra_data->flags & PCRE_EXTRA_MARK) != 0)
  *(extra_data->mark) = (pcre_uchar *)md->nomatch_mark;
#ifdef NO_RECURSE
  release_match_heapframes(&frame_zero);
#endif
return rc;
}