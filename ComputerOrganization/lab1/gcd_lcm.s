.data
	input_msg:	.asciiz "Please enter the first number: "
	input_msg2:	.asciiz "Please enter the second number: "
    space:      .asciiz " "
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
	move    $t0, $v0      		# store input in $t0 (set a)

# print input_msg2 on the console interface
	li      $v0, 4				# call system call: print string
	la      $a0, input_msg2		# load address of string into $a0
	syscall                 	# run the syscall
 
# read the input integer in $v0
	li      $v0, 5          	# call system call: read integer
	syscall                 	# run the syscall
	move    $t1, $v0      		# store input in $t1 (set b)

# jump to procedure gcd
    move    $a0, $t0  			# a -> a0
    move    $a1, $t1  			# b -> a1
	jal 	gcd
	move 	$a2, $v0			# save return value in a2 (because v0 will be used by system call) 

# jump to procedure lcm
	jal 	lcm
	move 	$t0, $v0			# save return value in t0 (because v0 will be used by system call) 

# print the result of procedure gcd on the console interface
	li 		$v0, 1				# call system call: print int
	move 	$a0, $a2			# move value of integer into $a0
	syscall 					# run the syscall

# print a newline at the end
	li		$v0, 4				# call system call: print string
	la		$a0, space  		# load address of string into $a0
	syscall						# run the syscall

# print the result of procedure lcm on the console interface
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

#------------------------- procedure gcd -----------------------------
# load argument n in $a0,$a1, return value in $v0. 
.text
gcd:	
    move    $s0, $a0            # i = a
    bge     $a1, $a0, check     # if  b >= a, jump to loop
    move    $s0, $a1            # i = b

check:
    blez    $s0, return_one     # 如果 i <= 0，返回 1

loop:
    # a % i
    div     $a0, $s0         	# a / i
    mfhi    $t0              	# t0 = a % i

    # b % i
    div     $a1, $s0         	# b / i
    mfhi    $t1              	# t1 = b % i

    # if (a%i == 0 && b%i == 0) return i;
    bne     $t0, $zero, next_i
    bne     $t1, $zero, next_i
    move    $v0, $s0         	# v0 = i (GCD found)
    j       done

next_i:
    addi    $s0, $s0, -1
    bgtz    $s0, loop           # if i > 0, continue loop

return_one:
    li      $v0, 1              # return 1

done:
	jr 		$ra					# return to the caller


#------------------------- procedure lcm -----------------------------
# a0 -> a
# a1 -> b
# a2 -> gcd ans
.text
lcm:	
	mul 	$v0, $a0, $a1		# lcm = (a*b)/gcd
    div		$v0, $a2			
    mflo	$v0					# $v0 = lcm
	jr 		$ra					# return to caller
