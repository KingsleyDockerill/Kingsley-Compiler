.text
a:
	.ascii "5"
b:
	.ascii "6"
c:
	.ascii "7"
.global _start
_start:
	MOV R7, #1
	SWI 0
_putnumb0
	MOV R7, #4
	MOV R0, #1
	MOV R2, #1000 @ MAX NUM LEN 1000
	LDR R1, =a
	SWI 0
_putnumb1
	MOV R7, #4
	MOV R0, #1
	MOV R2, #1000 @ MAX NUM LEN 1000
	LDR R1, =b
	SWI 0
_putnumb2
	MOV R7, #4
	MOV R0, #1
	MOV R2, #1000 @ MAX NUM LEN 1000
	LDR R1, =c
	SWI 0
