.data
	input_msg:	.asciiz "Enter an integer: "
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
	move    $a0, $v0      		# store input in $a0

# jump to procedure sumdigits
    jal     sumdigits           
    move    $a1, $v0            # save return value in a1

# print the result of procedure factorial on the console interface
	li 		$v0, 1				# call system call: print int
	move 	$a0, $a1			# move value of integer into $a0
	syscall 					# run the syscall

# print a newline at the end
	li		$v0, 4				# call system call: print string
	la		$a0, newline		# load address of string into $a0
	syscall						# run the syscall

# exit the program
	li 		$v0, 10				# call system call: exit
	syscall						# run the syscall

#------------------------- procedure sum digits -----------------------------
# $a0 digit
.text
sumdigits:
    li      $t0, 10             # $t0 = 10
    li      $v0, 0              # sum = 0

loop:
    blez    $a0, done           # if(n <= 0) done
    div     $a0, $t0            # n / 10
    mflo    $a0                 # n = n / 10
    mfhi    $t2                 # t2 = n % 10
    add     $v0, $v0, $t2       # sum += t2
    j		loop				# jump to loop

done:
	jr 		$ra					# return to the caller