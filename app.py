from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import mysql.connector

app = Flask(__name__)
app.secret_key = 'Pradhip@123'
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="farmer"
)
cursor = connection.cursor()
nav_bar = [
    {'url': '/', 'text': 'Home'},
    {'url': '/about', 'text': 'About'},
    {'url': '/contact', 'text': 'Contact'},
    # Add more navigation items as needed
]

# Define a simple footer
footer_info = "© 2024 Your Company. All rights reserved."

# Home Page
@app.route('/')
def home():
    if session:
        return redirect(url_for('index'))
    else:  
        return render_template('index.html')

# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if session:
        return redirect(url_for('user_home'))   
    else:

        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            # Your login logic here
            if verify_user_credentials(username, password):
                query = "SELECT * FROM register WHERE name = %s AND password = %s"
                cursor.execute(query, (username, password))
                result = cursor.fetchone()
                user_id=result[0]
                session['user_id'] = user_id

                # Redirect to the user's home page or any other page as needed
                return redirect(url_for('user_home'))
            else:
                # Display an error message (customize this part as needed)
                error_message = 'Invalid username or password. Please try again.'
                return render_template('login.html', error_message=error_message)
        # Your login logic here
    return render_template('login.html')

def verify_user_credentials(username, password):
    # Query to check user credentials
    query = "SELECT * FROM register WHERE name = %s AND password = %s"
    cursor.execute(query, (username, password))
    result = cursor.fetchone()
    return result is not None
def verify_admin_credentials(username, password):
    # Query to check user credentials
    query = "SELECT * FROM admin WHERE username = %s AND password = %s"
    cursor.execute(query, (username, password))
    result = cursor.fetchone()
    return result is not None


#user home page
@app.route('/user_home')
def user_home():
    if len(session) == 0:
        return redirect(url_for('login'))
    return render_template('user_home.html')

# User update profile details page
@app.route('/update_profile', methods=['GET', 'POST'])
def update_profile():
    if len(session) == 0:
        return redirect(url_for('login'))
    user_id = session.get('user_id')
    if request.method == 'GET':
        # If it's a GET request, fetch the user details based on a condition
        select_query = "SELECT * FROM register WHERE id=%s"
        cursor.execute(select_query, (user_id,))
        user = cursor.fetchone()  # Assuming there is only one user with the given condition
        return render_template('update_profile.html', user=user)

    elif request.method == 'POST':
        # If it's a POST request, handle the form submission and update the user details
        name = request.form['name']
        email = request.form['email']
        address = request.form['address']
        phone = request.form['phone']
        password = request.form['password']
        update_query = """
            UPDATE register
            SET email=%s, address=%s, phone=%s, password=%s
            WHERE id=%s
        """
        cursor.execute(update_query, (email, address, phone, password, user_id))
        connection.commit()

        # Fetch the updated user details
        select_query = "SELECT * FROM register WHERE id=%s"
        cursor.execute(select_query, (user_id,))
        user = cursor.fetchone()
    return render_template('update_profile.html', user=user)

# %user details the get details
@app.route('/display_profile')
def display_profile():
    if len(session) == 0:
        return redirect(url_for('login'))
    user_id = session.get('user_id')
    # Retrieve products from the add_product table
    select_query = "SELECT * FROM register where id=%s"
    cursor.execute(select_query, (user_id,))
    user = cursor.fetchone()
    return render_template ('display_profile.html',user=user)


#forgot password
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')

        # Check if the provided email exists in the dummy data
        user = next((user for user in users if user["email"] == email), None)
        if user:
            # Send password reset email or perform necessary actions
            # In a real application, you would typically send an email with a unique link for password reset
            return render_template('password_reset_sent.html', email=email)

    # If the request method is GET or the email is not found, render the forgot password form
    return render_template('forgot_password.html')


# Register Page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        address = request.form['address']
        phone = request.form['phone']
        password1 = request.form['password']
        confirm_password = request.form['confirm_password']

        # Perform validation
        if password1 != confirm_password:
            return render_template('register.html', error='Passwords do not match')

        # Create a new user and add it to the database
        # Example values stored in a list of tuples
        data_to_insert = [(name, email, phone, password1, address)]

        # SQL query with correct column names
        insert_query = """
            INSERT INTO register (name, email, phone, password, address)
                VALUES (%s, %s, %s, %s, %s)
        """

        # Execute the query with a single set of parameters
        cursor.executemany(insert_query, data_to_insert)

        connection.commit()
        return render_template('register.html')

    return render_template('register.html')




# Admin login page
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Your login logic here
        if verify_admin_credentials(username, password):
            # Redirect to the user's home page or any other page as needed
            session['user_id'] = username
            return redirect(url_for('admin_home'))
        else:
            # Display an error message (customize this part as needed)
            error_message = 'Invalid username or password. Please try again.'
            return render_template('admin_login.html', error_message=error_message)
    return render_template('admin_login.html')

# Admin home page
@app.route('/admin_home')
def admin_home():
    # You can perform any additional logic needed for the admin home page
    return render_template('admin_home.html')

def verify_admin_credentials(username, password):
    # Query to check admin credentials
    query = "SELECT * FROM admin WHERE username = %s AND password = %s"
    cursor.execute(query, (username, password))
    result = cursor.fetchone()
    if result is not None:
        return result
    else:
        return "Error: Result is none"
    
# Back button functionality
@app.route('/admin_home')
def menu():
    # Assuming you want to go back to the user home page
    return render_template('admin_home.html')

# Add Product Page
@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['vegetable_name']
        price = request.form['price']
        quality = request.form['quality']
        typ=request.form['Type']
        descript=request.form['description']
        

        # Handle file upload
        if 'image' in request.files:
            image = request.files['image']
            # You may want to validate and save the file to a specific directory
            # For simplicity, we'll just print the filename for now
            print("Uploaded image:", image.filename)

        # Perform database insertion
        insert_query = """
            INSERT INTO add_product (name, price, quality, image, type,description)
            VALUES (%s, %s, %s, %s,%s,%s)
        """
        # Execute the query with a single set of parameters
        cursor.execute(insert_query, (name, price, quality, image.filename,typ,descript))

        connection.commit()

        # Redirect to a page displaying the added product or any other page as needed.
        return redirect(url_for('add_product'))
        
    return render_template('add_product.html')  
 
@app.route('/admin_view_booking')
def admin_view_booking():
    # Select all data from the cart table
    select_query = "SELECT * FROM cart where status='1'"
    cursor.execute(select_query)
    cart_data = cursor.fetchall()

    # Initialize lists to store cart items, product details, and customer details
    cart_items = []
    product_details = []
    customer_details = []

    # Iterate through each item in the cart to fetch corresponding details
    for item in cart_data:
        # Fetch product details from add_product table based on the product id
        select_product_query = "SELECT * FROM add_product WHERE id = %s"
        cursor.execute(select_product_query, (item[1],))
        product_detail = cursor.fetchone()
        product_details.append(product_detail)

        # Fetch customer details from the register table based on the customer id
        select_customer_query = "SELECT * FROM register WHERE id = %s"
        cursor.execute(select_customer_query, (item[3],))
        customer_detail = cursor.fetchone()
        customer_details.append(customer_detail)

        # Append cart item along with product and customer details
        cart_items.append({
            'cart_id': item[0],
            'product_detail': product_detail,
            'customer_detail': customer_detail,
            'quantity': item[2],
            'status': item[4]
        })

    return render_template('admin_view_booking.html', cart_items=cart_items)

@app.route('/admin_view_customer')
def admin_view_customer():
    try:
        # Fetch all user details from the register table
        select_query = "SELECT * FROM register"
        cursor.execute(select_query)
        user_details = cursor.fetchall()

        return render_template('admin_view_customer.html', user_details=user_details)
    
    except Exception as e:
        # Handle the exception (e.g., log the error)
        print(f"Error: {e}")
        return render_template('error.html')  # You can create an error template

# Add this route to your existing

@app.route('/update_order_status', methods=['POST'])
def update_order_status():
    if request.method == 'POST':
        # Get the parameters from the POST request
        product_id = request.form.get('productId')
        customer_id = request.form.get('customerId')
        new_status = request.form.get('status')

        try:
            # Update the status in the cart table
            update_query = "UPDATE cart SET status = %s WHERE pid = %s AND cid = %s"
            cursor.execute(update_query, (new_status, product_id, customer_id))
            connection.commit()

            response = {'status': 'success', 'message': 'Order status updated successfully'}
            return redirect(url_for('admin_view_booking'))
        except Exception as e:
            connection.rollback()
            response = {'status': 'error', 'message': f'Error updating order status: {str(e)}'}

        return jsonify(response)
    else:
        # Handle non-POST requests accordingly
        return jsonify({'status': 'error', 'message': 'Invalid request method'})


@app.route('/view_product', methods=['GET', 'POST'])
def view_product():
    if len(session) == 0:
        return redirect(url_for('login'))

    # cart = dict()
    if request.method == 'POST':
        action = request.form.get('action')  # Add this line to get the action from the form
        if action == 'filter':
            try:
                # Retrieve the value of 'product_type' from the form data
                name = request.form.get('product_type')

                if name is None:
                    # Handle the case where 'product_type' is missing
                    return render_template('view_product.html', error_message='Product type is required')

                # Retrieve products from the add_product table
                select_query = "SELECT * FROM add_product WHERE type = %s"
                cursor.execute(select_query, (name,))
                products = cursor.fetchall()

                return render_template('view_product.html', products=products, name=name)

            except Exception as e:
                # Handle database or query errors
                return render_template('view_product.html', error_message=f'Error: {str(e)}')
        elif action == 'add':
            try:
                product_id = request.form.get('id')
                nos = request.form.get('nos')
                status = '0'
                data_to_insert = [(product_id, nos, session.get('user_id'), status)]
                
                # SQL query with correct column names
                insert_query = """
                        INSERT INTO cart (pid, nos, cid, status) VALUES (%s, %s, %s, %s)"""

                # Execute the query with a single set of parameters
                cursor.executemany(insert_query, data_to_insert)

                connection.commit()
                return redirect(url_for('view_product'))

            except ValueError:
                flash('Invalid quantity', 'error')
                return redirect(url_for('view_product'))

   
    return render_template('view_product.html')


#CART PAGE USER USEING THE POSTION
@app.route('/cart')
def cart():
    cart = []

    cid = session.get('user_id')
    
    # Select items from the cart table for the current user
    select_query = "SELECT * FROM cart WHERE cid = %s AND status='0'"
    cursor.execute(select_query, (cid,))
    cart = cursor.fetchall()
    
    # Initialize lists to store product details and total costs
    product_details = []
    total_costs = []
    
    # Iterate through each item in the cart to fetch corresponding product details
    for item in cart:
        # Fetch product details from add_product table based on the product id
        select_querys = "SELECT * FROM add_product WHERE id = %s"
        cursor.execute(select_querys, (item[1], ))
        product_detail = cursor.fetchone()
        product_details.append(product_detail)
        
        # Calculate total cost for the current item (quantity * price)
        total_cost = int(item[2]) * float(product_detail[2])  # Assuming product price is stored in the third column of add_product table
        total_costs.append(total_cost)
        
    # Render the cart.html template with cart items, product details, and total costs
    return render_template('cart.html', cart=cart, product_details=product_details, total_costs=total_costs)


# Add the following route to handle item cart remove item
@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    if len(session) == 0:
        return redirect(url_for('login'))

    # Get the cart_id from the form data
    cart_id = request.form.get('cart_id')

    # Check if the user is logged in
    if 'user_id' in session:
        # Remove the item from the cart table based on cart_id
        user_id = session['user_id']
        delete_query = "DELETE FROM cart WHERE cid = %s AND cartid = %s"
        cursor.execute(delete_query, (user_id, cart_id))
        connection.commit()

    return redirect(url_for('cart'))


# User home page
@app.route('/back')
def back():
    return render_template('user_home.html')

# "View Product Page only admin show the page" 
@app.route('/products', methods=['GET', 'POST'])
def products():
    if len(session) == 0:
        return redirect(url_for('index'))
    if request.method == 'POST':
        try:
            # Retrieve the value of 'product_type' from the form data
            name = request.form.get('product_type')
            if name is None:
                # Handle the case where 'product_type' is missing
                return render_template('products.html', error_message='Product type is required')
            # Retrieve products from the add_product table
            select_query = "SELECT * FROM add_product"
            cursor.execute(select_query)
            products = cursor.fetchall()
            # Filter products based on the selected product type
            filtered_products = [product for product in products if product[6] == name]
            return render_template('products.html', products=filtered_products, name=name)

        except Exception as e:
            # Handle database or query errors
            return render_template('products.html', error_message=f'Error: {str(e)}')

    # If it's not a POST request or an error occurred, show all products
    select_query = "SELECT * FROM add_product"
    cursor.execute(select_query)
    products = cursor.fetchall()
    return render_template('products.html', products=products)

#get product 
def get_products(product_type):
    try:
        query = "SELECT * FROM add_product WHERE type = %s"
        cursor.execute(query, (product_type,))
        product_list = cursor.fetchall()
        return product_list

    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()


@app.route('/edit_product', methods=['GET', 'POST'])
def edit_product():

    if request.method == 'POST':
        try:
            # Retrieve the value of 'product_type' from the form data
            name = request.form.get('product_type')
            try:
                action = request.form.get('action')
                product_id = request.form.get('product_id')

                if action == 'edit':
                    # Store the product_id in a session variable and redirect to update_product.html
                    session['edit_product_id'] = product_id
                    return redirect(url_for('update_product'))
                elif action == 'delete':
                    # Delete the corresponding product from the database
                    delete_query = f"DELETE FROM add_product WHERE id = {product_id}"
                    cursor.execute(delete_query)
                    connection.commit()
                    # After deletion, retrieve updated product list
                    select_query = "SELECT * FROM add_product"
                    cursor.execute(select_query)
                    products = cursor.fetchall()

                    # Filter products based on the selected product type
                    filtered_products = [product for product in products if product[6] == name]

                    return render_template('edit_product.html', products=filtered_products, name=name)

            except Exception as e:
                # Handle database or query errors
                return render_template('edit_product.html', error_message=f'Error: {str(e)}')

        except Exception as e:
            # Handle other errors
            return render_template('edit_product.html', error_message=f'Error: {str(e)}')

    # If it's not a POST request or an error occurred, show all products
    select_query = "SELECT * FROM add_product"
    cursor.execute(select_query)
    products = cursor.fetchall()
    return render_template('edit_product.html', products=products)



#update product in admin login function 
@app.route('/update_product', methods=['GET', 'POST'])
def update_product():
    user=[]
    
    product_id = session.get('edit_product_id')
    if request.method == 'GET':
        # If it's a GET request, fetch the user details based on a condition
      
        select_query = "SELECT * FROM add_product WHERE id=%s"
        cursor.execute(select_query, (product_id,))

        user = cursor.fetchone()  # Assuming there is only one user with the given condition

        return render_template('update_product.html', user=user)

    elif request.method == 'POST':
        # If it's a POST request, handle the form submission and update the user details
        name = request.form['name']
        price = request.form['price']
        quality = request.form['quality']
        description = request.form['description']

       
        product_type = request.form['type']
        # Update user details in the database
        update_query = f"""
            UPDATE add_product
            SET name = '{name}', price = '{price}', quality = '{quality}',
                 description = '{discription}',
                type = '{product_type}'
            WHERE id = {product_id}
        """
        cursor.execute(update_query)
        connection.commit()

        # Fetch the updated user details
        select_query = "SELECT * FROM add_product WHERE id=%s"
        cursor.execute(select_query, (product_id,))
        user = cursor.fetchone()

        return render_template('update_product.html', user=user)

# Implement a function to save the uploaded image and return its path
def save_uploaded_image(image):
    if image and allowed_file(image.filename):
        filename = secure_filename(image.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(image_path)
        return image_path
# Implement a function to check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
#user details the get details

#ORDER PAGE A USER USED FUNCTION

@app.route('/order', methods=['GET', 'POST'])
def order():
    if request.method == 'POST':
        user_id = session.get('user_id')
        st = "1"
        order_datetime = request.form.get('orderDateTime')

        try:
            # Update the cart status and set the delivery date and time
            query = "UPDATE cart SET status = %s, delivery_datetime = %s WHERE cid = %s"
            cursor.execute(query, (st, order_datetime, user_id,))
            connection.commit()
            return redirect('final_order')

        except Exception as e:
            # Print the error message to understand the issue
            print(f"Error: {e}")
            return redirect(url_for('final_order'))

    return render_template(url_for('order.html'))

    
@app.route('/final_order')
def cart_order():
    cart = []

    cid = session.get('user_id')
    
    # Select items from the cart table for the current user
    select_query = "SELECT * FROM cart WHERE cid = %s AND status='1'"
    cursor.execute(select_query, (cid,))
    cart = cursor.fetchall()
    
    # Initialize lists to store product details and total costs
    product_details = []
    total_costs = []
    
    # Iterate through each item in the cart to fetch corresponding product details
    for item in cart:
        # Fetch product details from add_product table based on the product id
        select_querys = "SELECT * FROM add_product WHERE id = %s"
        cursor.execute(select_querys, (item[1], ))
        product_detail = cursor.fetchone()
        product_details.append(product_detail)
        
        # Calculate total cost for the current item (quantity * price)
        total_cost = int(item[2]) * float(product_detail[2])  # Assuming product price is stored in the third column of add_product table
        total_costs.append(total_cost)
    
    # Render the cart.html template with cart items, product details, and total costs
    return render_template('order.html', cart=cart, product_details=product_details, total_costs=total_costs)


#logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))
# Route for the about page
@app.route('/about')
def about():
    return render_template('about.html', nav_bar=nav_bar, footer_info=footer_info)

if __name__ == '__main__':
    app.run(debug=True)
