.data
	input_msg:	.asciiz "Enter five positive integers: "
    space:      .asciiz " "
	newline: 	.asciiz "\n"
    arr:    .word 0,0,0,0,0

.text
.globl main
#------------------------- main -----------------------------
main:
# print input_msg on the console interface
	li      $v0, 4				# call system call: print string
	la      $a0, input_msg		# load address of string into $a0
	syscall                 	# run the syscall

# 讀取 5 個整數
    la      $a0, arr            # $a0 指向陣列起始地址
    li      $t1, 5              # 設定迴圈計數

read_loop:
    li      $v0, 5              # 讀取整數
    syscall
    sw      $v0, 0($a0)         # 存入陣列
    addi    $a0, $a0, 4         # 移動到下一個元素
    addi    $t1, $t1, -1        # 減少計數
    bnez    $t1, read_loop      # 若未讀完，繼續

# prepare for min,max space
    la      $a0, arr            # 陣列起始地址
    li      $a1, 5              # 陣列大小
    addi    $sp, $sp, -8        # 分配空間給 max 和 min
    move    $a2, $sp            # max 
    addi    $a3, $sp, 4         # min 
    jal     findMaxMin          # 呼叫函式

# print the max
    lw 		$a0, 0($a2)         # move value of max into $a0
	li 		$v0, 1				# call system call: print int			
	syscall 					# run the syscall

# print a newline at the end
	li		$v0, 4				# call system call: print string
	la		$a0, space  		# load address of string into $a0
	syscall						# run the syscall

# print the min
    lw 		$a0, 0($a3)         # move value of min into $a0
	li 		$v0, 1				# call system call: print int
	syscall 					# run the syscall

# print a newline at the end
	li		$v0, 4				# call system call: print string
	la		$a0, newline		# load address of string into $a0
	syscall						# run the syscall

# exit the program
	li 		$v0, 10				# call system call: exit
	syscall						# run the syscall

#------------------------- procedure findMaxMin -----------------------------
# $a0 陣列起始地址
# $a1 陣列大小
# $a2 max 
# $a3 min 
# $t1 i
.text
findMaxMin:	
	addi 	$sp, $sp, -4		# adiust stack for ra
	sw 		$ra, 0($sp)			# save the return address

    # 初始化 max 和 min
    lw      $t0, 0($a0)         # $t0 = arr[0]
    sw      $t0, 0($a2)         # max = arr[0]
    sw      $t0, 0($a3)         # min = arr[0]
    addi    $a0, $a0, 4         # $a0 = arr[0]+1
    li      $t1, 1              # i = 1

findloop:
    bge     $t1, $a1, done
    lw      $t2, 0($a0)         # $t2 = arr[i]
max:
    lw      $t3, 0($a2)
    blt     $t2, $t3, min
    sw      $t2, 0($a2)
min:
    lw      $t3, 0($a3)
    bgt     $t2, $t3, iplus
    sw      $t2, 0($a3)

iplus:
    addi    $a0, $a0, 4         # $a0 = arr[0]+1
    addi    $t1, $t1, 1         # i++
    j       findloop

done:
    lw      $ra, 0($sp)
    addi 	$sp, $sp, 4
    jr      $ra


    
