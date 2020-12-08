.text:
a:
	.ascii "5\n"
b:
	.ascii "6\n"
c:
	.ascii "Hello, world!"
d:
	.ascii "This"
e:
	.ascii " is "
f:
	.ascii "putc"
g:
	.ascii "har\n"
h:
	.ascii ""
.global _start:
_start:
	MOV R7, #1
	SWI 0
_putnumb0:
	MOV R7, #4
	MOV R0, #1
	MOV R2, #1000 @ MAX NUM LEN 1000
	LDR R1, =a
	SWI 0
_putnumb1:
	MOV R7, #4
	MOV R0, #1
	MOV R2, #1000 @ MAX NUM LEN 1000
	LDR R1, =b
	SWI 0
_putstr0:
	MOV R7, #4
	MOV R0, #1
	MOV R2, #1000 @ MAX NUM LEN 10000
	LDR R1, =c
	SWI 0
_putchar0:
	MOV R7, #4
	MOV R0, #1
	MOV R2, #10000 @ MAX NUM LEN 10000
	LDR R1, =d
	SWI 0
_putchar1:
	MOV R7, #4
	MOV R0, #1
	MOV R2, #10000 @ MAX NUM LEN 10000
	LDR R1, =e
	SWI 0
_putchar2:
	MOV R7, #4
	MOV R0, #1
	MOV R2, #10000 @ MAX NUM LEN 10000
	LDR R1, =f
	SWI 0
_putchar3:
	MOV R7, #4
	MOV R0, #1
	MOV R2, #10000 @ MAX NUM LEN 10000
	LDR R1, =g
	SWI 0
_getstr0:
	MOV R7, #3
	MOV R0, #0
	MOV R2, #10000 @ MAX NUM LEN 10000
	LDR R1, =h
	SWI 0
_putstr1:
	MOV R7, #4
	MOV R0, #1
	MOV R2, #1000 @ MAX NUM LEN 10000
	LDR R1, =h
	SWI 0
