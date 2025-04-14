def solve_tridiagonal(d, a, c): # 總共 8n-7個運算
    n = len(d)
    # Forward elimination # 形成上三角矩陣 # 5n-5個運算
    for i in range(1, n): # n-1圈
        mult = a[i-1] / d[i-1] # 用上一行把下對角線消掉 # 1除
        d[i] = d[i] - mult * a[i-1] # 1乘 + 1減
        c[i] = c[i] - mult * c[i-1] # 1乘 + 1減

    # Back substitution # 由後往回代 # 3n−2個運算
    x = [0] * n
    x[-1] = round(c[-1] / d[-1], 3) # 1除
    for i in range(n-2, -1, -1): # n-1圈
        x[i] = (c[i] - a[i] * x[i+1]) / d[i] # 1乘 + 1減 + 1除
        x[i] = round(x[i],3)
    
    return x

d = [4, 4, 4, 4, 4, 4]
a = [-1, -1, -1, -1, -1]
c = [100, 200, 200, 200, 200, 100]
ans = solve_tridiagonal(d, a, c)
print(ans)


#  [ d  a  0  0  c
#    a  d  a  0  c
#    0  a  d  a  c
#    0  0  a  d  c ]

# 3(n−1)+1=3n−2