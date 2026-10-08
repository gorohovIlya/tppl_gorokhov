section .data

    format_result db "%s: %ld", 10, 0

    format_corrupted db "%s: файл испорчен", 10, 0

section .bss

    buffer resb 4096

    x_array resq 1024

section .text

    extern printf

    global main

print_corrupted:

    lea rdi, [rel format_corrupted]

    mov rsi, r12

    xor eax, eax

    call printf

    ret

parse_number:

.parse_spaces:

    cmp byte [rsi], ' '

    jne .check_minus

    inc rsi

    jmp .parse_spaces

.check_minus:

    xor r8d, r8d

    cmp byte [rsi], '-'

    jne .check_digit

    mov r8d, 1

    inc rsi

.check_digit:

    movzx rcx, byte [rsi]

    cmp rcx, '0'
    jb .error

    cmp rcx, '9'
    ja .error

    xor eax, eax

.parse_digit:

    movzx rcx, byte [rsi]

    cmp rcx, '0'
    jb .number_finished

    cmp rcx, '9'
    ja .number_finished

    imul rax, 10

    sub rcx, '0'

    add rax, rcx

    inc rsi

    jmp .parse_digit

.number_finished:

    cmp r8d, 1

    jne .success

    neg rax

.success:

    clc

    ret

.error:

    stc

    ret

main:

    push rbp
    mov rbp, rsp

    mov r13, rsi

    cmp rdi, 2

    jne .wrong_arguments

    mov r12, [r13 + 8]

    mov rax, 2

    mov rdi, r12

    xor esi, esi

    xor edx, edx

    syscall

    test rax, rax

    js .corrupted

    mov r14, rax

    xor eax, eax

    mov rdi, r14

    lea rsi, [rel buffer]

    mov edx, 4096

    syscall

    test rax, rax

    jle .close_and_corrupted

    mov r15, rax

    mov byte [buffer + r15], 0

    mov rax, 3

    mov rdi, r14

    syscall

    lea rsi, [rel buffer]

    xor edi, edi

.read_x:

    cmp byte [rsi], 0
    je .corrupted

    cmp byte [rsi], 10
    je .corrupted

    cmp byte [rsi], 13
    je .corrupted

    call parse_number

    jc .corrupted

    cmp rdi, 1024

    jae .corrupted

    mov [x_array + rdi * 8], rax

    inc rdi

    cmp byte [rsi], ','

    je .x_comma

    cmp byte [rsi], ' '

    je .x_spaces

    cmp byte [rsi], 10

    je .start_y

    cmp byte [rsi], 13

    je .start_y

    cmp byte [rsi], 0

    je .corrupted

    jmp .corrupted

.x_comma:

    inc rsi

    jmp .read_x

.x_spaces:

    inc rsi

    jmp .x_spaces_check

.x_spaces_check:

    cmp byte [rsi], ' '

    je .x_spaces_more

    cmp byte [rsi], ','

    je .x_comma

    cmp byte [rsi], 10

    je .start_y

    cmp byte [rsi], 13

    je .start_y

    jmp .corrupted

.x_spaces_more:

    inc rsi

    jmp .x_spaces_check

.start_y:

    mov r13, rdi

    cmp byte [rsi], 13

    jne .check_y_newline

    inc rsi

.check_y_newline:

    cmp byte [rsi], 10

    jne .prepare_y

    inc rsi

.prepare_y:

    cmp byte [rsi], 0

    je .corrupted

    xor edi, edi

    xor r14, r14

.read_y:

    cmp rdi, r13

    jae .check_file_end

    call parse_number

    jc .corrupted

    mov rcx, [x_array + rdi * 8]

    sub rcx, rax

    add r14, rcx

    inc rdi

    cmp byte [rsi], ','

    je .y_comma

    cmp byte [rsi], ' '

    je .y_spaces

    cmp byte [rsi], 0

    je .calculate_average

    cmp byte [rsi], 10

    je .calculate_average

    cmp byte [rsi], 13

    je .calculate_average

    jmp .corrupted

.y_comma:

    inc rsi

    jmp .read_y

.y_spaces:

    inc rsi

    jmp .y_spaces_check

.y_spaces_check:

    cmp byte [rsi], ' '

    je .y_more_spaces

    cmp byte [rsi], ','

    je .y_comma

    cmp byte [rsi], 0

    je .calculate_average

    cmp byte [rsi], 10

    je .calculate_average

    cmp byte [rsi], 13

    je .calculate_average

    jmp .corrupted

.y_more_spaces:

    inc rsi

    jmp .y_spaces_check

.check_file_end:

.check_file_end_loop:

    cmp byte [rsi], ' '

    je .check_file_end_skip

    cmp byte [rsi], 10

    je .calculate_average

    cmp byte [rsi], 13

    je .calculate_average

    cmp byte [rsi], 0

    je .calculate_average

    jmp .corrupted

.check_file_end_skip:

    inc rsi

    jmp .check_file_end_loop

.calculate_average:

    mov rax, r14

    cqo

    idiv r13

    lea rdi, [rel format_result]

    mov rsi, r12

    mov rdx, rax

    xor eax, eax

    call printf

    xor eax, eax

    leave
    ret

.corrupted:

    call print_corrupted

    mov eax, 1

    leave
    ret

.close_and_corrupted:

    mov rbx, rax

    mov rax, 3

    mov rdi, r14

    syscall

    call print_corrupted

    mov eax, 1

    leave
    ret

.wrong_arguments:

    mov eax, 1

    leave
    ret
