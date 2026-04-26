 
'''
users

| user_id | name | city | signup_date |

orders

| order_id | user_id | amount | order_date |

payments

| payment_id | order_id | status |

'''
#1

#Find users who have never made any order.


'''
SELECT u.user_id , u.name , o.order_id 
FROM users u 
LEFT JOIN orders o
ON u.order_id = o.order_id
WHERE o.order_id IS NULL

'''
#---------------------------
#2

#Find users who made orders
#but none of their orders were paid.

'''
SELECT o.user_id , p.order_id , p.status 
FROM orders o 
LEFT JOIN payments p
ON o.order_id = p.order_id
WHERE p.order_id IS NOT NULL
AND p.status = 'failed'

'''
#----------------------------

#3

#For each user, show: total orders AND total paid orders


'''
SELECT o.user_id , COUNT(DISTINCT o.order_id) AS total_orders ,
p.status , 
CASE 
WHEN p.status = 'paid' THEN COUNT(DISTINCT o.order_id)
ELSE 0
FROM orders o
LEFT JOIN payments p
ON o.order_id = p.order_id
GROUP BY o.user_id

'''
#------------------------------

'''
users

| user_id | name | city | signup_date |

orders

| order_id | user_id | amount | order_date |

payments

| payment_id | order_id | status |

'''

#4 Find users whose average order 
#amount is greater than the overall average.

'''
SELECT user_id ,
SUM(amount) / COUNT(DISTINCT order_id) AS ova,
FROM orders
WHERE ova > (
SELECT SUM(amount) / COUNT(order_id) AS overall_average 
FROM orders)

'''
#----------------------------

#Show the first and last order date for each user.

'''
SELECT user_id , MIN(order_date) AS earliest_order ,
MAX(order_date) AS newest_order
FROM orders 
GROUP BY user_id

'''
#-----------------------------
#Find users who made more than 2 orders in a single month.

'''
SELECT user_id,
       MONTH(order_date) AS month_order,
       COUNT(order_id) AS num_orders
FROM orders
GROUP BY user_id, MONTH(order_date)
HAVING COUNT(order_id) > 2 
'''
#-----------------------------
#Rank orders for each user based on amount.
'''
SELECT user_id,
       order_id,
       amount,
       RANK() OVER (
           PARTITION BY user_id
           ORDER BY amount DESC
       ) AS rnk
FROM orders
'''
#-------------------------------

#Show the difference between 
#current and previous order amount for each user.

'''
SELECT user_id,
       order_id,
       amount,
       amount - LAG(amount) OVER (
           PARTITION BY user_id
           ORDER BY order_date
       ) AS diff
FROM orders
'''
#-------------------------------

#Find the top 1 order per user (highest amount).

'''
WITH t AS (
SELECT user_id,
       order_id,
       amount,
       RANK() OVER (
           PARTITION BY user_id
           ORDER BY amount DESC
       ) AS rnk
FROM orders
)
SELECT *
FROM t
WHERE rnk = 1

'''
#--------------------------------
#Find users whose last order is also their highest order

'''
WITH t AS(
SELECT user_id , order_id , amount ,
RANK() OVER(
PARTITION BY user_id 
ORDER BY amount DESC , order_date DESC) AS highest_lastOrder
FROM orders 
)
SELECT * FROM t 
WHERE highest_lastOrder =1

'''

#Find users who have not made any purchase 
# in the last 30 days but made purchases before that.


#Find the percentage of paid orders out of total orders.

'''
SELECT o.user_id,
COUNT(CASE WHEN p.status = 'paid' THEN 1 END) * 100.0
/ COUNT(*) AS paid_percentage
FROM orders o
LEFT JOIN payments p
ON o.order_id = p.order_id
GROUP BY o.user_id

'''
#---------------------------------

#For each month, calculate:
#total revenue
#number of users

'''
SELECT 
      MONTH(o.order_date) AS month , COUNT(o.user_id) AS num_users ,
      COUNT(o.order_id) * SUM(o.amount) AS total_revenue
FROM orders o
LEFT JOIN payments p
ON o.order_id = p.order_id
WHERE p.status = 'paid'

'''

#==============================================
#==============================================
#==============================================
#==============================================
#==============================================
#==============================================
#==============================================
#==============================================
#==============================================

#DATASET

'''
USERS

user_id INT
name VARCHAR
city VARCHAR
signup_date DATE
---

ORDERS 

order_id INT
user_id INT
amount DECIMAL
order_date DATE

---

PAYMENTS

payment_id INT
order_id INT
status VARCHAR   -- ('paid', 'failed')
payment_method VARCHAR

'''
#-----------------------------
#-----------------------------
#1
#-- Get all users from 'Cairo'

'''
SELECT * 
FROM users 
WHERE city = 'Cairo'

'''
#-----------------------
#2
#-- Get all orders with amount greater than 500
'''
SELECT * 
FROM orders
WHERE amount > 500

'''
#-----------------------
#3
#-- Get all paid payments
'''
SELECT * 
FROM payments
WHERE status ='paid'
'''
#-----------------------
#4
#-- Get all users who signed up after '2023-01-01'
'''
SELECT user_id , name , signup_date
FROM users 
WHERE signup_date > '2023-01-01'
'''
#-----------------------
#5
#-- Get all orders between '2023-01-01' and '2023-03-01' 
'''
SELECT * 
FROM orders 
WHERE order_date BETWEEN '2023-01-01' and '2023-03-01'
'''
#-----------------------
#6
#-- Get unique cities from users table
'''
SELECT user_id, DISTINCT City
FROM users
'''
#-----------------------
#7
#-- Count number of users
'''
SELECT COUNT(user_id) AS num_users
FROM users
'''
#-----------------------
#8
#-- Count number of orders per user
'''
SELECT user_id , COUNT(order_id) AS num_orders 
FROM orders
GROUP BY user_id
'''
#-----------------------
#9
#-- Calculate total revenue (all orders)
'''
SELECT order_id , SUM(amount) AS total_revenue
FROM orders
'''
#-----------------------
#10
#-- Find average order amount
'''
SELECT order_id ,AVG(amount) AS ave_amount
FROM orders 
'''
#-----------------------
#11
#-- Find users who made more than 3 orders
'''
SELECT user_id , COUNT(DISTINCT order_id) AS num_orders
FROM orders
GROUP BY user_id
HAVING COUNT(DISTINCT order_id) > 3
'''
#-----------------------
#12
#-- Calculate total revenue per month
'''
SELECT MONTH(order_date) AS month_order , SUM(amount) AS total_revenue
FROM orders
GROUP BY month_order
'''
#-----------------------
#13
#-- Count number of users per city
'''
SELECT City , COUNT(user_id) AS num_users
FROM users
GROUP BY City
'''
#-----------------------
#14
#-- Find total paid revenue (only paid orders)
'''
SELECT SUM(o.amount) AS total_amount , p.status
FROM orders o
JOIN payments p
ON o.order_id = p.order_id
WHERE p.status = 'paid'

'''
#-----------------------
#15
#-- Find users who made orders but never paid
'''
SELECT o.user_id ,o.order_id, p.status
FROM orders o
LEFT JOIN payments p
ON o.order_id = p.order_id
WHERE p.order_id IS NOT NULL AND p.status ='failed'

'''
#-----------------------
#16
#-- Find users with no orders
'''
SELECT u.* , o.order_id
FROM users u
LEFT JOIN orders o
ON u.user_id = o.user_id 
WHERE o.order_id IS NULL 

'''
#----------------------
#17
#-- Find total number of orders per city
'''
SELECT u.City , COUNT(o.order_id) AS num_orders 
FROM users u
JOIN orders o
ON u.user_id = o.user_id
GROUP BY u.City
'''
#----------------------
#18
#-- Find top 5 users by total spending (paid only)
'''
SELECT o.user_id , SUM(o.amount) AS total_amount , p.status
FROM orders o
JOIN payments p
ON o.order_id = p.order_id
WHERE p.status = 'paid'
ORDER BY total_amount DESC
LIMIT 5 
'''
#-----------------------
#19
#-- For each user: -- total orders & -- total paid amount
'''
SELECT 
    o.user_id,
    COUNT(DISTINCT o.order_id) AS num_orders,
    SUM(CASE WHEN p.status = 'paid' THEN o.amount ELSE 0 END) AS total_paid
FROM orders o
LEFT JOIN payments p
ON o.order_id = p.order_id
GROUP BY o.user_id
'''

#===================================================
#===================================================
#===================================================
#===================================================
#===================================================
#===================================================

'''
users

(user_id, name, city, signup_date)

orders

(order_id, user_id, amount, order_date)

payments

(payment_id, order_id, status)

'''

#1
#-- Find the number of orders placed by each user in the last 30 days
'''
SELECT COUNT(DISTINCT order_id) AS num_orders , user_id ,
DATE_SUB(order_date,INTERVAL 30 DAY)
FROM orders
GROUP BY user_id
'''
#-----------------------
#2
#-- Find users who signed up but never placed any order
'''
SELECT u.user_id , u.signup_date , o.order_id
FROM users u 
LEFT JOIN orders o
ON u.user_id = o.user_id
WHERE o.order_id IS NULL
'''
#-----------------------
#3
#-- Find the total number of paid and failed payments
'''
SELECT COUNT(payment_id) AS num_payment ,status
FROM payments
GROUP BY status
'''
#-----------------------
#4
#-- Find the number of distinct users who made at least one paid order
'''
SELECT COUNT(DISTINCT o.user_id) AS num_user , p.status
FROM orders 
LEFT JOIN payments p
ON o.order_id = p.order_id
WHERE p.status ='paid' 

'''
#------------------------
#5
#-- Find the earliest signup date per city
'''
SELECT city , MIN(signup_date)
FROM users
GROUP BY city
'''
#------------------------
#6
#-- Calculate total revenue per user (only paid orders)
'''
SELECT o.user_id , SUM(o.amount) AS total_revenue
FROM orders o
LEFT JOIN payments p 
ON o.order_id = p.order_id
WHERE p.status = 'paid'
GROUP BY o.user_id
'''
#------------------------
#7 
#-- Find users whose total spending is greater than the average spending of all users
'''
SELECT user_id , SUM(amount) AS total_amount 
FROM orders
GROUP BY user_id
HAVING SUM(amount) > (SELECT AVG(amount) FROM orders GROUP BY user_id)
'''
#-------------------------
#8 xxxxxxxxxxxxxxxx
#-- Calculate the average number of orders per user
'''
SELECT AVG(amount) AS avg_amount , user_id
FROM orders 
GROUP BY user_id 
'''
#------------------------
#9
#-- Find the month with the highest total revenue
'''
SELECT SUM(amount) AS total_amount , MONTH(order_date) AS month 
FROM orders 
GROUP BY month 
ORDER BY total_amount DESC 
LIMIT 1
'''
#------------------------
#10
#-- For each city, find total number of users and total revenue
'''
SELECT COUNT(u.user_id) AS num_users , SUM(o.amount) AS total_revenue , u.city
FROM users u
LEFT JOIN orders o
ON u.user_id = o.user_id 
GROUP BY u.city
'''
#-------------------------
#11 xxxxxxxxxxxxxxxxxxxxxxxx
#-- Find users who made at least one order but all their payments failed
'''
SELECT o.user_id , o.order_id , p.status 
FROM orders o 
LEFT JOIN payments p 
ON o.order_id = p.order_id 
WHERE p.status = 'failed' AND p.order_id IS NOT NULL
'''
#HAVING SUM(CASE WHEN p.status = 'paid' THEN 1 ELSE 0 END) = 0 يعنى اية 
#-------------------------
#12
#-- Find users whose first order was a paid order
'''
WITH t AS (
SELECT o.user_id, o.order_id, p.status,
ROW_NUMBER() OVER(
PARTITION BY o.user_id
ORDER BY o.order_date
) AS rn
FROM orders o
JOIN payments p ON o.order_id = p.order_id
)
SELECT *
FROM t
WHERE rn = 1 AND status = 'paid'
'''
#-------------------------
#13
#-- Find users who never had a failed payment
'''
SELECT o.user_id
FROM orders o
JOIN payments p ON o.order_id = p.order_id
GROUP BY o.user_id
HAVING SUM(CASE WHEN p.status = 'failed' THEN 1 ELSE 0 END) = 0
'''
#--------------------------
#14 xxxxxxxxxxxxxxxxxxxxxxx
#-- Find total number of orders and paid orders per user
'''
SELECT COUNT(DISTINCT o.order_id) AS total_orders ,
COUNT(DISTINCT CASE WHEN p.status = 'paid' THEN o.order_id ELSE 0 END) AS paid_orders 
FROM orders o
LEFT JOIN payments p
ON o.order_id = p.order_id 
GROUP BY o.user_id 
'''
#COUNT(CASE WHEN p.status = 'paid' THEN 1 END) يعنى اية واية الفرق بين 0 و 1 وامتى 

#--------------------------
#15
#-- For each user, rank their orders by amount (highest first)
'''
SELECT user_id ,order_id,
RANK() OVER(
PARTITION BY user_id 
ORDER BY amount DESC) AS highest_orders
FROM orders 
'''
#-------------------------
#16
#-- Find the highest order per user
'''
WITH t AS(
SELECT user_id , order_id ,
ROW_NUMBER() OVER(
PARTITION BY user_id 
ORDER BY amount DESC) AS highest_order
FROM orders )
SELECT * FROM t 
WHERE highest_order =1
'''
#-------------------------
#17
#-- Find users whose last order amount is greater than their average order amount
'''
WITH t AS(
SELECT user_id , 

FIRST_VALUE(amount) OVER(
PARTITION BY user_id 
ORDER BY order_date DESC) AS last_amount ,
AVG(amount) OVER(
PARTITION BY user_id ) AS avg_amount
FROM orders )
SELECT * FROM t 
WHERE last_amount > avg_amount

'''
#18 xxxxxxxxxxxxxxxxx
#-- For each user:- total revenue - last order date - rank users globally based on revenue
'''
SELECT SUM(amount) OVER(
PARTITION BY user_id) AS total_revenue,
MAX(order_date) OVER(
PARTITION BY user_id) AS last_order ,
RANK() OVER(
PARTITION BY user_id 
ORDER BY amount DESC) users_rnk
FROM orders
'''
#=======================================
#=======================================
#=======================================
#=======================================
#=======================================
#=======================================
#=======================================



# 🧠 SECTION 1 — Business SQL



### Q1
#-- Write a query to calculate the conversion rate:
#-- (number of users who made at least one paid order) / (total users)

"""
SELECT COUNT(DISTINCT CASE WHEN p.status = 'paid' THEN o.user_id ELSE 0 END) AS num_users / COUNT(DISTINCT o.user_id) AS total_users
FROM orders o
LEFT JOIN payments p
ON o.order_id = p.order_id 

"""

#-------------------------------
### Q2


#-- Find the retention rate between January and February:
#-- users who ordered in Jan AND also ordered in Feb
"""
SELECT user_id , MONTH(order_date) AS month 
FROM orders 
GROUP BY user_id 
HAVING CASE WHEN month = 1 AND month = 2 THEN 1 ELSE 0 
"""


#------------------------------

### Q3

#-- Calculate ARPU (Average Revenue Per User)
#-- considering only paid orders
"""
SELECT SUM(CASE WHEN p.status ='paid' THEN o.amount END 0) / COUNT(DISTINCT o.user_id) AS arpu
FROM orders o
JOIN payments p
ON o.order_id = p.order_id

"""

#-------------------------------

### Q4


#-- Find the percentage of users who never placed any order
"""
SELECT COUNT(CASE WHEN order_id IS NULL THEN user_id END 0) / COUNT(user_id) * 100
FROM orders 
"""
#------------------------------

### Q5


#-- Find the churned users:
#-- users who placed orders before but not in the last 60 days
"""
SELECT user_id , MONTH(order_date) AS month
FROM orders 
GROUP BY user_id
HAVING DATESUB(CURDATE() - INTERVAL 60 DAY )
"""

#---------------------------------------
#---------------------------------------
#---------------------------------------
#---------------------------------------
#18/4/2026
#---------------------------------------
#---------------------------------------
#---------------------------------------
#---------------------------------------

### Q6

#-- Find users who have orders but all their payments failed
"""
SELECT o.user_id , o.order_id
FROM orders o
JOIN payments p
ON o.order_id = p.order_id
GROUP BY o.user_id
HAVING SUM(CASE WHEN p.status ='paid' THEN 1 ELSE 0 END) = 0 
"""

#-------------------------------

### Q7
#-- Find users who have at least one paid order and one failed order
"""
SELECT u.user_id 
FROM orders o
LEFT JOIN payments p  
ON o.order_id = p.order_id 
GROUP BY o.user_id
HAVING SUM(CASE WHEN p.status = 'faild' THEN 1 ELSE 0 END) > 0
AND SUM(CASE WHEN p.status ='paid' THEN 1 ELSE 0 END ) > 0 
"""



### Q8


#-- Find users whose first order was NOT paid
"""
SELECT user_id

FROM (SELECT o.user_id , p.status ,
ROW_NUMBER() OVER(PARTITION BY o.user_id 
ORDER BY order_date ASC ) AS rn
FROM orders o
JOIN payments p
ON o.order_id = p.order_id
) t
WHERE rn = 1 
AND status <> 'paid'  

"""
#------------------------

### Q9


#-- Find users whose last order was failed

"""
SELECT user_id

FROM (
    SELECT o.user_id,
           p.status,
           ROW_NUMBER() OVER (
               PARTITION BY o.user_id 
               ORDER BY o.order_date DESC
           ) AS rn
    FROM orders o
    JOIN payments p
        ON o.order_id = p.order_id
) t

WHERE rn = 1
  AND status = 'failed'
"""
#--------------------------------

### Q10


#-- Find users who made more than 5 orders but total revenue < 1000
"""
SELECT user_id , COUNT(order_id) AS num_orders , SUM(amount) AS total_spending
FROM orders 
GROUP BY user_id
HAVING COUNT(order_id) > 5
AND SUM(amount) < 1000
"""

#--------------------------------

# 💣 SECTION 3 — Window Functions (INTERVIEW FAVORITE)

### Q11

#-- Rank users globally based on total revenue
"""
SELECT u.user_id ,SUM(o.amount) AS total_spend, 
RANK() OVER(
ORDER BY SUM(o.amount) DESC) AS rnk
FROM users u 
LEFT JOIN orders o
ON u.user_id = o.user_id 

"""

#------------------------------

### Q12


#-- For each user, show the previous order amount and calculate the difference
"""
SELECT 
    user_id,
    amount,
    LAG(amount) OVER (
        PARTITION BY user_id
        ORDER BY order_date
    ) AS prev_amount,
    
    amount - LAG(amount) OVER (
        PARTITION BY user_id
        ORDER BY order_date
    ) AS diff_amount
FROM orders;
"""

#-------------------------------

### Q13


#-- Find the top 2 highest orders per user
"""
SELECT user_id , SUM(amount) AS total_amount , order_id
FROM orders
GROUP BY user_id
ORDER BY total_amount DESC
LIMIT 2
"""

#------------------------------

### Q14

#-- Find users whose latest order is their highest order
"""
WITH t AS (
SELECT user_id , order_id , amount , order_date,
ROW_NUMBER() OVER(
PARTITION BY user_id
ORDER BY order_date DESC) AS 
)
"""



# 💣 SECTION 4 — Real Analytics Thinking


### Q16


#-- Find the month-over-month growth in revenue

"""
WITH monthly AS (
    SELECT 
        DATE_TRUNC('month', order_date) AS month,
        SUM(amount) AS total_revenue
    FROM orders
    GROUP BY month
)
SELECT 
    month,
    total_revenue,
    LAG(total_revenue) OVER (ORDER BY month) AS prev_month_revenue,
    total_revenue - LAG(total_revenue) OVER (ORDER BY month) AS growth
FROM monthly
"""


#------------------------

### Q17


#-- Find the top 3 cities by total revenue

"""
WITH top_cities AS (
    SELECT u.city,
           SUM(o.amount) AS total_revenue
    FROM users u
    LEFT JOIN orders o
        ON u.user_id = o.user_id
    GROUP BY u.city
),
ranked AS (
    SELECT city,
           total_revenue,
           DENSE_RANK() OVER (
               ORDER BY total_revenue DESC
           ) AS rnk
    FROM top_cities
)
SELECT city, total_revenue
FROM ranked
WHERE rnk <= 3
"""
#------------------------

### Q18


#-- Find users who increased their spending compared to their previous order

'''
WITH t AS (
    SELECT user_id,
           order_date,
           amount,
           LAG(amount) OVER (
               PARTITION BY user_id
               ORDER BY order_date
           ) AS prev_amount
    FROM orders
)
SELECT DISTINCT user_id
FROM t
WHERE amount > prev_amount
'''

#---------------------------

### Q20


#-- Build a user summary table:
#-- user_id
#-- total_orders
#-- total_paid_revenue
#-- last_order_date
#-- user_rank based on revenue


'''
WITH user_summary AS (
    SELECT u.user_id,
           COUNT(o.order_id) AS total_orders,
           SUM(CASE WHEN o.status = 'paid' THEN o.amount ELSE 0 END) AS total_paid_revenue,
           MAX(o.order_date) AS last_order_date
    FROM users u
    LEFT JOIN orders o
        ON u.user_id = o.user_id
    GROUP BY u.user_id
)
SELECT user_id,
       total_orders,
       total_paid_revenue,
       last_order_date,
       RANK() OVER (ORDER BY total_paid_revenue DESC) AS user_rank
FROM user_summary
'''

#===================================
#===================================
#===================================
#===================================
#===================================
#===================================
#1

'''
SELECT d.department_name , AVG(e.salary) AS avg_salary
FROM Departments d 
LEFT JOIN Employees e
ON e.id = d.id
GROUP BY d.department_name 
HAVING AVG(e.sala
WITH USER_SUMMARY AS (SELECT u.user_id , 
COUNT(o.order_id) AS total_orders ,
SUM(o.ary) > 5000
'''

#--------------------------
#2
'''
SELECT employee_id ,
DENSE_RANK() OVER(
PARTITION BY department_id
ORDER BY sale_amount DESC) 
FROM Sales 

'''

#----------------------------
#3
'''
SELECT emp.name AS Employee_Name
FROM Employees emp
JOIN Employees mgr ON emp.manager_id = mgr.id
WHERE emp.salary > mgr.salary
'''

#----------------------------
#4
'''
SELECT customer_id , SUM(order_value) AS total_spent
CASE
WHEN order_value > 10000 THEN "VIP"
WHEN order_value BETWEEN 5000 AND 10000 THEN "Premium"
ELSE "Standard" END 0 AS cat_customers
FROM orders
GROUP BY customer_id
'''
#-------------------------------------------
#-------------------------------------------
#-------------------------------------------
#-------------------------------------------
#-------------------------------------------
#-------------------------------------------

#1
 
'''
SELECT user_id , DATE(login_date) AS date
FROM Logins
WHERE login_date >= DATE_SUB(CURDATE(), INTERVAL 3 DAY)
GROUP BY user_id
'''

'''
WITH t AS(

SELECT user_id , DATE(login_date) AS date
LAG(login_date) OVER(
PARTITION BY user_id) AS fir_user,

LEAD(login_date) OVER(
PARTITION BY user_id
) AS sec_user ,

LEAD(login_date) OVER(
PARTITION BY user_id)

FROM Logins)
SELECT * FROM t
WHERE fir_user IS NOT NULL
AND sec_user IS NOT NULL 
AND third_user IS NOT NULL 

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'''
'''WITH login_ranks AS (
    SELECT 
        user_id, 
        login_date,
        -- بنجيب اليوم اللي قبل الحالي واليوم اللي بعده
        LAG(login_date, 1) OVER (PARTITION BY user_id ORDER BY login_date) AS prev_day,
        LEAD(login_date, 1) OVER (PARTITION BY user_id ORDER BY login_date) AS next_day
    FROM (SELECT DISTINCT user_id, login_date FROM Logins) AS clean_data -- شلنا التكرار في نفس اليوم
)
SELECT DISTINCT user_id
FROM login_ranks
WHERE DATEDIFF(login_date, prev_day) = 1  -- اليوم الحالي ناقص اللي قبله = 1
  AND DATEDIFF(next_day, login_date) = 1; -- اللي بعده ناقص الحالي = 1
  '''

#--------------------------
#3
'''
SELECT 
    sale_date,
    amount,
    AVG(amount) OVER (
        ORDER BY sale_date 
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS rolling_avg_7d
FROM Daily_Sales
'''
#==========================================
#==========================================
#==========================================
#==========================================
#==========================================
#==========================================
#1
'''
Given a table orders(user_id, order_id, amount, order_date),
write a query to return the top 3 highest orders for each user based on amount
'''

'''
WITH t AS(
SELECT user_id , order_id , SUM(amount) AS total_amount,
DENSE_RANK() OVER(PARTITION BY user_id 
ORDER BY amount DESC) AS top_highest_order
FROM orders 
) 
SELECT * FROM t
WHERE top_highest_order <=3
'''

#---------------------------

'''
Given tables orders(order_id, user_id, order_date) and payments(order_id, status),
return the latest order for each user and its payment status
'''

'''
WITH t AS(

SELECT o.user_id , p.status , 
ROW_NUMBER() OVER(
PARTITION BY o.user_id 
ORDER BY o.order_date DESC) AS latest_order
FROM orders o 
LEFT JOIN payments p
ON o.order_id = p.order_id
)
SELECT * FROM t
WHERE latest_order = 1

'''

#-----------------------------

'''
Given a table payments(user_id, status),
find users who have at least one 'paid' and one 'failed' transaction.
'''

'''
SELECT user_id , status 
FROM payments 
GROUP BY user_id
HAVING SUM(CASE WHEN status = 'paid' THEN 1 ELSE 0 END) > 0
AND SUM(CASE WHEN status ='failed' THEN 1 ELSE 0 END ) > 0 
'''

#----------------------------
'''
Given a table transactions(user_id, transaction_date, amount),
calculate the running total of amount for each user ordered by date.
'''
'''
SELECT user_id ,
SUM(amount) OVER(
PARTITION BY user_id 
ORDER BY transiction_date DESC) AS running_total
FROM transictions 

'''
#---------------------------

'''
Given a table orders(user_id, order_date, amount),
for each order, return:

the previous order amount
and the difference between current and previous order

'''

'''
WITH t AS(
SELECT user_id ,amount ,LAG(amount) OVER(
PARTITION BY user_id 
ORDER BY order_date ASC) AS previous_order ,
)
SELECT 
previous_order , amount - previous_order
FROM t

'''