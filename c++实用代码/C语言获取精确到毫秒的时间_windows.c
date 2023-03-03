
time_t gettimeofday(unsigned int *usecs)
{
	FILETIME ft;
	unsigned __int64 tmpres = 0;
	time_t t = 0;

	GetSystemTimeAsFileTime(&ft);

	tmpres |= ft.dwHighDateTime;
	tmpres <<= 32;
	tmpres |= ft.dwLowDateTime;

	tmpres /= 10; /*convert into microseconds*/
	/*converting file time to unix epoch*/
	tmpres -= 11644473600000000Ui64;

	if(usecs) *usecs = (unsigned int)(tmpres % 1000000UL);
	t = (time_t)(tmpres / 1000000UL);
	return t;
}