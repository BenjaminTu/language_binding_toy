namespace com.aws.ffi

// AWS_CRT_API void aws_crt_init(void);
operation aws_crt_init {
    input: void,
    output: void
}

// AWS_CRT_API void aws_crt_clean_up(void);
operation aws_crt_clean_up {
    input: void,
    output: void
}

// AWS_CRT_API int aws_crt_test_error(int err);
structure aws_crt_test_error_input {
    err: int32_t
}

structure aws_crt_test_error_output {
    ret: int32_t
}

operation aws_crt_test_error {
    input: aws_crt_test_error_input,
    output: aws_crt_test_error_output
}

// AWS_CRT_API aws_crt_allocator *aws_crt_default_allocator(void);
structure aws_crt_default_allocator_output {
    ret: aws_crt_allocator
}

operation aws_crt_default_allocator {
    input: void,
    output: aws_crt_default_allocator_output
}

// AWS_CRT_API void *aws_crt_mem_acquire(size_t size);
structure aws_crt_mem_acquire_input {
    size: size_t
}

structure aws_crt_mem_acquire_output {
    @pointer
    ret: void
}

operation aws_crt_mem_acquire {
    input: aws_crt_mem_acquire_input,
    output: aws_crt_mem_acquire_output
}

// AWS_CRT_API void aws_crt_mem_release(void *mem);
structure aws_crt_mem_release_input {
    @pointer
    mem: void
}

operation aws_crt_mem_release {
    input: aws_crt_mem_release_input,
    output: void
}

// AWS_CRT_API uint64_t aws_crt_mem_bytes(void);
structure aws_crt_mem_bytes_output {
    ret: uint64_t
}

operation aws_crt_mem_bytes {
    input: void,
    output: aws_crt_mem_bytes_output
}

// AWS_CRT_API uint64_t aws_crt_mem_count(void);
structure aws_crt_mem_count_output {
    ret: uint64_t
}

operation aws_crt_mem_count {
    input: void,
    output: aws_crt_mem_count_output
}

// AWS_CRT_API void aws_crt_mem_dump(void);
operation aws_crt_mem_dump {
    input: void,
    output: void
}