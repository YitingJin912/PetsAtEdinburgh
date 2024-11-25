from flask import Flask, render_template, request, redirect, session, url_for
import mysql.connector


app = Flask(__name__, static_folder='static', static_url_path='/static')


app.secret_key = 'admin'




MYSQL_HOST = 'localhost'
MYSQL_USER = 'papikorg_website'
MYSQL_PASSWORD = '!kPk*UwDnP0;'
MYSQL_DB = 'papikorg_petsatedinburgh'


def get_db_connection():
    return mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB
    )
    
    





@app.route('/admin_users')
def admin_users():
    if not session.get('admin_logged_in'):
        return redirect('/login')

    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch user data
    cursor.execute("SELECT * FROM users")
    data = cursor.fetchall()

    # Close the database connection
    cursor.close()
    conn.close()

    # Render admin user page
    return render_template('admin_user.html', data=data)





@app.route('/update_user', methods=['POST'])
def update_user():
    user_id = request.form.get('user_id')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            # Pass user details to the update form
            return render_template('update_user.html', user=user)
        else:
            return "User not found", 404
    except Exception as e:
        print(f"Error fetching user: {e}")
        return f"An error occurred: {e}", 500
        
        


@app.route('/submit_update_user', methods=['POST'])
def submit_update_user():
    user_id = request.form.get('user_id')
    name = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET username=%s, password=%s, email=%s WHERE id=%s",
            (name, password, email, user_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/admin_users')  # Redirect back to the admin page
    except Exception as e:
        print(f"Error updating user: {e}")
        return f"An error occurred: {e}", 500




@app.route('/delete_user', methods=['POST'])
def delete_user():
    user_id = request.form.get('user_id')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            # Pass user details to the update form
            return render_template('delete_user.html', user=user)
        else:
            return "User not found", 404
    except Exception as e:
        print(f"Error fetching user: {e}")
        return f"An error occurred: {e}", 500
        
        
        
    
@app.route('/submit_delete_user', methods=['POST'])
def submit_delete_user():
    user_id = request.form.get('user_id')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id=%s", (user_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/admin_users')  # Redirect back to the admin page
    except Exception as e:
        print(f"Error deleting user: {e}")
        return f"An error occurred: {e}", 500



@app.route('/add_user', methods=['POST'])
def add_user():
    if request.method == 'POST':
        try:
            # Retrieve form data
            username = request.form.get('newusername')
            password = request.form.get('newpassword')
            email = request.form.get('newemail')

            # Connect to the database
            conn = get_db_connection()
            cursor = conn.cursor()

            # Insert user into the database
            query = "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)"
            cursor.execute(query, (username, password, email))
            conn.commit()

            # Close connections
            cursor.close()
            conn.close()

            # Redirect to admin user page
            return redirect('/admin_users')  # Ensure '/admin_user' is a valid route in your app

        except Exception as e:
            print(f"Error adding user: {e}")
            return f"An error occurred: {e}", 500

    return redirect('/admin_users') 





@app.route('/admin_products')
def admin_products():
    if not session.get('admin_logged_in'):
        return redirect('/login')
        
        
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    data = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('admin_products.html', data=data)
    
    
    
    


@app.route('/update_product', methods=['POST'])
def update_product():
    product_id = request.form.get('product_id')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products WHERE id=%s", (product_id,))
        product = cursor.fetchone()
        cursor.close()
        conn.close()

        if product:
            # Pass product details to the update form
            return render_template('update_product.html', product=product)
        else:
            return "Product not found", 404
    except Exception as e:
        print(f"Error fetching products: {e}")
        return f"An error occurred: {e}", 500   
        
 
 
@app.route('/submit_update_product', methods=['POST'])
def submit_update_product():
    product_id = request.form.get('product_id')
    name = request.form.get('name')
    description = request.form.get('description')
    image = request.form.get('image')
    price = request.form.get('price')
    stock = request.form.get('stock')
    category = request.form.get('category')
    status = request.form.get('status')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE products SET name=%s, description=%s, image=%s, price=%s, stock=%s, category=%s, status=%s WHERE id=%s",
            (name, description, image, price, stock, category, status, product_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/admin_products')  # Redirect back to the admin page
    except Exception as e:
        print(f"Error updating product: {e}")
        return f"An error occurred: {e}", 500        
        
        


@app.route('/delete_product', methods=['POST'])
def delete_product():
    product_id = request.form.get('product_id')
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products WHERE id=%s", (product_id,))
        product = cursor.fetchone()
        cursor.close()
        conn.close()

        if product:
            # Pass product details to the update form
            return render_template('delete_product.html', product=product)
        else:
            return "Product not found", 404
    except Exception as e:
        print(f"Error fetching products: {e}")
        return f"An error occurred: {e}", 500  
        
        
        
        
@app.route('/submit_delete_product', methods=['POST'])
def submit_delete_product():
    product_id = request.form.get('product_id')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM products WHERE id=%s", (product_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/admin_products')  # Redirect back to the admin page
    except Exception as e:
        print(f"Error deleting product: {e}")
        return f"An error occurred: {e}", 500


        
        
    
    
@app.route('/add_product', methods=['POST'])
def add_product():
    if request.method == 'POST':
        try:
            # Retrieve form data
            name = request.form.get('newname')
            description = request.form.get('newdescription')
            image = request.form.get('newimage')
            price = request.form.get('newprice')
            stock = request.form.get('newstock')
            category = request.form.get('newcategory')
            status = request.form.get('newstatus')


            # Connect to the database
            conn = get_db_connection()
            cursor = conn.cursor()

            # Insert product into the database
            query = "INSERT INTO products (name, description, image, price, stock, category, status) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (name, description, image, price, stock, category, status))
            conn.commit()

            # Close connections
            cursor.close()
            conn.close()

            # Redirect to admin product page
            return redirect('/admin_products')  # Ensure '/admin_products' is a valid route in your app

        except Exception as e:
            print(f"Error adding product: {e}")
            return f"An error occurred: {e}", 500

    return redirect('/admin_products')  



@app.route('/admin_orders')
def admin_orders():
    if not session.get('admin_logged_in'):
        return redirect('/login')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders")
    data = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('admin_order.html', data=data)
  


@app.route('/delete_order', methods=['POST'])
def delete_order():
    try:
        order_id = request.form.get('order_id')
        if not order_id:
            return "Order ID is required", 400

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM orders WHERE id=%s", (order_id,))
        order = cursor.fetchone()
        cursor.close()
        conn.close()

        if order:
            return render_template('delete_order.html', order=order)
        else:
            return "Order not found", 404
    except Exception as e:
        print(f"Error fetching order: {e}")
        return f"An error occurred: {e}", 500 
        
    

@app.route('/submit_delete_order', methods=['POST'])
def submit_delete_order():
    try:
        # Get the order_id from the form
        order_id = request.form.get('order_id')
        
        if not order_id:
            return "Order ID is required", 400

        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Delete the order items related to this order
        delete_order_items_query = "DELETE FROM order_items WHERE order_id = %s"
        cursor.execute(delete_order_items_query, (order_id,))

        # Delete the order from the database
        delete_query = "DELETE FROM orders WHERE id = %s"
        cursor.execute(delete_query, (order_id,))

        # Commit the changes and close the connection
        conn.commit()
        cursor.close()
        conn.close()

        # Redirect back to the admin orders page
        return redirect(url_for('admin_orders'))

    except Exception as e:
        print(f"Error occurred while deleting the order: {e}")
        return f"An error occurred: {e}", 500
        
        

@app.route('/')
def index():
    return render_template('index.html') 
    
    
    
@app.route('/home')
def home():
    if not session.get('user_logged_in'):
        return redirect('/login')
        
    return render_template('home.html')    


   
@app.route('/shop')
def shop():
    if not session.get('user_logged_in'):
        return redirect('/login')    
    
    return render_template('shop.html') 
   
   
   
@app.route('/about')
def about():
    if not session.get('user_logged_in'):
        return redirect('/login')    
        
    return render_template('about.html') 
    
    
    
@app.route('/help')
def help():
    if not session.get('user_logged_in'):
        return redirect('/login')    
        
    return render_template('help.html') 
    
    
    
@app.route('/contact')
def contact():
    if not session.get('user_logged_in'):
        return redirect('/login')    
        
    return render_template('contact.html') 
    
    
    
    
@app.route('/thanks', methods=['GET', 'POST'])
def thanks():
        
    return render_template('thanks.html')     
    



@app.route('/privacy_policy')
def privacy_policy():
    
    return render_template('privacy_policy.html')
    
    
    
    
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            email = request.form.get('email')



            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("INSERT INTO users (username, password, email) VALUES (%s, %s, %s)", (username, password, email))
            conn.commit()


            cursor.close()
            conn.close()

            return redirect('/login')

    return render_template('Register.html')
    
    

    
    

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Retrieve form data
        username = request.form.get('username')
        password = request.form.get('password')
        
        
        if username == 'admin' and password == 'secret':
                session['admin_logged_in'] = True
                return redirect('/admin_users')

        try:
            # Database connection
            conn = get_db_connection()
            cursor = conn.cursor()

            # Execute SELECT query
            query = "SELECT * FROM users WHERE username=%s AND password=%s"
            cursor.execute(query, (username, password))
            user = cursor.fetchone()

            # Close database connection
            cursor.close()
            conn.close()


            if user:
                session['user_logged_in'] = True
                return redirect('/home')
            else:
                return "Invalid username or password"
        except Exception as e:
            print(f"Error occurred during login: {e}")
            return f"An error occurred: {e}", 500
            
            


    return render_template('Sign_in.html')




@app.route('/logout')
def logout():
    # Clear the session
    session.clear()
    return redirect('/')
    
    
    
        
   
@app.route('/cat')
def cat():
    if not session.get('user_logged_in'):
        return redirect('/login')
        
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = "SELECT * FROM products WHERE category = %s"
        cursor.execute(query, ('cat',)) 
        cats = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return render_template('cat_page.html', cats=cats)
    
    
    except Exception as e:
        print(f"Error occurred while fetching cats: {e}")
        return f"An error occurred: {e}", 500

    
    

@app.route('/dog')
def dog():
    if not session.get('user_logged_in'):
        return redirect('/login')
        
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        

        query = "SELECT * FROM products WHERE category = %s"
        cursor.execute(query, ('dog',))
        dogs = cursor.fetchall()
        
        cursor.close()
        conn.close()
    
        return render_template('dog_page.html', dogs=dogs)
    
    except Exception as e:
        print(f"Error occurred while fetching dogs: {e}")
        return f"An error occurred: {e}", 500
    

    
@app.route('/bird')
def bird():
    if not session.get('user_logged_in'):
        return redirect('/login')
        
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        

        query = "SELECT * FROM products WHERE category = %s"
        cursor.execute(query, ('bird',))
        birds = cursor.fetchall()
        
        cursor.close()
        conn.close()
        

        
        # Return template with birds
        return render_template('bird_page.html', birds=birds)
    except Exception as e:
        print(f"Error occurred while fetching birds: {e}")
        return f"An error occurred: {e}", 500






@app.route('/individual_product/<int:product_id>')
def individual_product(product_id):
    if not session.get('user_logged_in'):
        return redirect('/login')
        
    try:
        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Fetch product details from the database
        query = "SELECT * FROM products WHERE id = %s"
        cursor.execute(query, (product_id,))
        product = cursor.fetchone()

        # Close the database connection
        cursor.close()
        conn.close()

        # Check if the product exists
        if not product:
            return "Product not found", 404

        # Render the template with product data
        return render_template('individual_product.html', product={
            'id': product[0],
            'name': product[1],
            'description': product[2],
            'image': product[3],
            'price': product[4],
            'stock': product[5],
            'category': product[6],
            'status': product[7],
        })

    except Exception as e:
        print(f"Error occurred: {e}")
        return f"An error occurred: {e}", 500    
    



@app.route('/add_to_basket', methods=['POST'])
def add_to_basket():

        
    product_id = request.form.get('product_id')
    quantity = int(request.form.get('quantity', 1))
    if 'basket' not in session:
        session['basket'] = {}
    if product_id in session['basket']:
        session['basket'][product_id] += quantity
    else:
        session['basket'][product_id] = quantity
    session.modified = True
    print("Basket after adding item:", session['basket'])
    return redirect(url_for('basket'))
    
    
    
@app.route('/basket')
def basket():
    if not session.get('user_logged_in'):
        return redirect('/login')    
    
    try:
        print("Session basket:", session.get('basket'))  # Debug session basket
        basket_data = []
        total = 0

        if 'basket' in session and session['basket']:
            conn = get_db_connection()
            cursor = conn.cursor()
            for product_id, quantity in session['basket'].items():
                query = "SELECT id, name, price, image FROM products WHERE id = %s"
                cursor.execute(query, (product_id,))
                product = cursor.fetchone()
                
                if product:
                    subtotal = round(float(product[2]) * quantity, 2)
                    total += subtotal
                    basket_data.append({
                        'id': product[0],
                        'name': product[1],
                        'price': product[2],
                        'image': product[3],
                        'quantity': quantity,
                        'subtotal': subtotal
                    })
                else:
                    print(f"Product with ID {product_id} not found in database.")

            cursor.close()
            conn.close()
        else:
            # Basket is empty
            return render_template('basket.html', basket=[], total=0, message="Your basket is empty.")

        print("Basket data for template:", basket_data)
        print("Total:", total)
        return render_template('basket.html', basket=basket_data, total=round(total, 2), message=None)

    except Exception as e:
        # Log the error and return a 500 error response
        print(f"Error in /basket route: {e}")
        return "An internal error occurred.", 500



@app.route('/checkout', methods=['POST'])
def checkout():
        
    try:
        # Check if the basket exists in the session
        if 'basket' not in session or not session['basket']:
            return "Basket is empty. Please add items before checkout.", 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # Fetch basket details
        basket_data = []
        total = 0
        for product_id, quantity in session['basket'].items():
            query = "SELECT id, name, price FROM products WHERE id = %s"
            cursor.execute(query, (product_id,))
            product = cursor.fetchone()
            if product:
                subtotal = float(product[2]) * quantity
                total += subtotal
                basket_data.append({
                    'id': product[0],
                    'name': product[1],
                    'price': product[2],
                    'quantity': quantity,
                    'subtotal': subtotal
                })

        # Save the order details in the database
        order_query = """
            INSERT INTO orders (total_amount, created_at)
            VALUES (%s, NOW())
            RETURNING id
        """
        cursor.execute(order_query, (total,))
        order_id = cursor.fetchone()[0]

        # Save order items in the database
        for item in basket_data:
            order_item_query = """
                INSERT INTO order_items (order_id, product_id, name, quantity, price, subtotal)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(order_item_query, (
                order_id, item['id'], item['name'], item['quantity'],item['price'], item['subtotal']
            ))

        conn.commit()

        # Clear the basket from the session after checkout
        session.pop('basket', None)
        session.modified = True

        cursor.close()
        conn.close()

        return render_template('checkout_success.html', order_id=order_id, total=round(total, 2))
    except Exception as e:
        print(f"Error during checkout: {e}")
        return f"An error occurred during checkout: {e}", 500    




        
    
if __name__ == '__main__':
    app.run(debug=True)