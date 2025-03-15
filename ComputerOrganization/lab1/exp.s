.data
	input_msg:	.asciiz "Enter base (positive integers): "
	input_msg2:	.asciiz "Enter exponent (positive integers): "
	newline: 	.asciiz "\n"

.text
.globl main
#------------------------- main -----------------------------
main:
# print input_msg on the console interface
	li      $v0, 4				# call system call: print string
	la      $a0, input_msg		# load address of string into $a0
	syscall                 	# run the syscall
 
# read the input integer in $v0
	li      $v0, 5          	# call system call: read integer
	syscall                 	# run the syscall
	move    $t0, $v0      		# store input in $t0 (set arugument of base)

# print input_msg2 on the console interface
	li      $v0, 4				# call system call: print string
	la      $a0, input_msg2		# load address of string into $a0
	syscall                 	# run the syscall
 
# read the input integer in $v0
	li      $v0, 5          	# call system call: read integer
	syscall                 	# run the syscall
	move    $t1, $v0      		# store input in $t1 (set arugument of exponent)

# jump to procedure exp
    move    $a0, $t0  # base -> a0
    move    $a1, $t1  # exp -> a1
	jal 	exp
	move 	$t0, $v0			# save return value in t0 (because v0 will be used by system call) 

# print the result of procedure factorial on the console interface
	li 		$v0, 1				# call system call: print int
	move 	$a0, $t0			# move value of integer into $a0
	syscall 					# run the syscall

# print a newline at the end
	li		$v0, 4				# call system call: print string
	la		$a0, newline		# load address of string into $a0
	syscall						# run the syscall

# exit the program
	li 		$v0, 10				# call system call: exit
	syscall						# run the syscall

#------------------------- procedure exp -----------------------------
# load argument base,exponent in $a0,$a1, return value in $v0. 
.text
exp:	
	addi 	$sp, $sp, -12		# adjust stack for 3 items
	sw 		$ra, 8($sp)			# save the return address
	sw 		$a0, 4($sp)			# save the argument base
	sw 		$a1, 0($sp)			# save the argument exponent
	slti 	$t0, $a1, 1			# test for n < 1
	beq 	$t0, $zero, L1		# if n >= 1 go to L1
	addi 	$v0, $zero, 1		# return 1
	addi 	$sp, $sp, 12		# pop 3 items off stack
	jr 		$ra					# return to caller
L1:		
	addi 	$a1, $a1, -1		# n >= 1, argument gets (n-1)
	jal 	exp			        # call exp with (n-1)
	lw 		$a0, 4($sp)			# return from jal, restore argument base
	lw 		$a1, 0($sp)			# return from jal, restore argument exponent
	lw 		$ra, 8($sp)			# restore the return address
	addi 	$sp, $sp, 12		# adjust stack pointer to pop 3 items
	mul 	$v0, $a0, $v0		# return base * exp(base, exp-1)
	jr 		$ra					# return to the caller
