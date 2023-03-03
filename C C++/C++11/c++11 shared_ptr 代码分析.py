类：
template<typename _Tp> 
class shared_ptr : public __shared_ptr<_Tp>
    构造：
    template<typename _Tp1>
	explicit shared_ptr(_Tp1* __p) : __shared_ptr<_Tp>(__p) { }
        类：
        template<typename _Tp, _Lock_policy _Lp>
        class __shared_ptr
            构造：
            template<typename _Tp1>
            explicit __shared_ptr(_Tp1* __p) : _M_ptr(__p), _M_refcount(__p)
            { 。。。 }
            成员：
            _Tp*	   	         _M_ptr;
            __shared_count<_Lp>  _M_refcount;  
                类：
                template<_Lock_policy _Lp>
                class __shared_count
                    构造：
                    template<typename _Ptr>  //这里的_Ptr类型，通常是根据参数__p推导出来的
                    explicit  __shared_count(_Ptr __p) : _M_pi(0)
                    {
                        __try
                        {
                          _M_pi = new _Sp_counted_ptr<_Ptr, _Lp>(__p);
                                类：
                                template<typename _Ptr, _Lock_policy _Lp>
                                class _Sp_counted_ptr final : public _Sp_counted_base<_Lp>
                                    构造：
                                    explicit  _Sp_counted_ptr(_Ptr __p) noexcept : _M_ptr(__p) { }
                                    成员：
                                    virtual void _M_destroy() noexcept { delete this; }
                                    virtual void _M_dispose() noexcept { delete _M_ptr; }
                                    _Ptr  _M_ptr;
                                    基类：
                                        template<_Lock_policy _Lp = __default_lock_policy>
                                        class _Sp_counted_base : public _Mutex_base<_Lp>
                                        构造：
                                        _Sp_counted_base() noexcept : _M_use_count(1), _M_weak_count(1) { }
                                        析构：
                                        void _M_release() noexcept
                                        {
                                            // Be race-detector-friendly.  For more info see bits/c++config.
                                            _GLIBCXX_SYNCHRONIZATION_HAPPENS_BEFORE(&_M_use_count);
                                            if (__gnu_cxx::__exchange_and_add_dispatch(&_M_use_count, -1) == 1)
                                            {
                                                _GLIBCXX_SYNCHRONIZATION_HAPPENS_AFTER(&_M_use_count);
                                                _M_dispose();
                                                // There must be a memory barrier between dispose() and destroy()
                                                // to ensure that the effects of dispose() are observed in the
                                                // thread that runs destroy().
                                                // See http://gcc.gnu.org/ml/libstdc++/2005-11/msg00136.html
                                                if (_Mutex_base<_Lp>::_S_need_barriers)
                                                {
                                                    _GLIBCXX_READ_MEM_BARRIER;
                                                    _GLIBCXX_WRITE_MEM_BARRIER;
                                                }
                                                // Be race-detector-friendly.  For more info see bits/c++config.
                                                _GLIBCXX_SYNCHRONIZATION_HAPPENS_BEFORE(&_M_weak_count);
                                                if (__gnu_cxx::__exchange_and_add_dispatch(&_M_weak_count, -1) == 1)
                                                {
                                                    _GLIBCXX_SYNCHRONIZATION_HAPPENS_AFTER(&_M_weak_count);
                                                    _M_destroy();
                                                }
                                            }
                                        }
                                        成员：
                                        _Atomic_word  _M_use_count;  
                                        _Atomic_word  _M_weak_count; 
                        }
                        __catch(...)
                        {
                          delete __p;
                          __throw_exception_again;
                        }
                    }
                    析构：
                    ~__shared_count() noexcept
                    {
                        if (_M_pi != nullptr)
                            _M_pi->_M_release();
                    }
                    成员：
                    _Sp_counted_base<_Lp>*  _M_pi;