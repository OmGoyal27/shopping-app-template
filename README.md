# Shopping Website Template

A modern, responsive shopping website template built with Flask and featuring a dark theme UI. This template provides a complete e-commerce foundation with product management, cart functionality, and search capabilities.

## Features

- 🛍️ **Product Catalog**: Display products with images, descriptions, and pricing
- 🛒 **Shopping Cart**: Add, update, and remove items from cart
- 🔍 **Search Functionality**: Search products by name and description
- 📱 **Responsive Design**: Mobile-friendly dark theme interface
- 🎨 **Modern UI**: Clean, professional styling with hover effects
- 📦 **Stock Management**: Automatic stock tracking and updates
- 🧾 **Checkout Process**: Complete purchase workflow

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**
   ```bash
   python app.py
   ```

3. **Open in Browser**
   Navigate to [http://localhost:5000](http://localhost:5000)

## Project Structure

```
Shopping website template/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── static/               # Static assets
│   ├── assets/          # Images and icons
│   └── styles/          # CSS stylesheets
├── templates/           # HTML templates
│   ├── index.html       # Homepage
│   ├── product.html     # Product details
│   ├── cart.html        # Shopping cart
│   └── checkout.html    # Checkout page
└── Products/            # Product data
    └── [Product Name]/  # Individual product folders
        ├── details.json # Product information
        └── assets/      # Product images
```

## Adding Products

### Step 1: Create Product Directory
Create a new folder in the `Products` directory. The folder name will be used in the product URL.

### Step 2: Add Product Details
Create a `details.json` file with the following structure:

```json
{
    "name": "Your Product Name",
    "price": 99.99,
    "description": "Detailed product description that will appear in search results and on the product page.",
    "images": [
        "image1.jpg",
        "image2.jpg"
    ],
    "stock": 25
}
```

### Step 3: Add Product Images
Place your product images in an `assets` folder within your product directory.

**Example Structure:**
```
Products/
└── Awesome Widget/
    ├── details.json
    └── assets/
        ├── widget-front.jpg
        └── widget-back.jpg
```

## Configuration

### Secret Key
Update the secret key in `app.py` for production use:
```python
app.secret_key = "your-secure-secret-key-here"
```

### Database Integration
Currently uses file-based JSON storage. For production, consider integrating with a database like SQLite or PostgreSQL.

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Homepage with all products |
| `/product/<name>` | GET | Individual product page |
| `/search` | GET | Search results |
| `/cart` | GET | Shopping cart |
| `/add_to_cart/<name>` | POST | Add item to cart |
| `/update_cart/<name>` | POST | Update cart quantity |
| `/remove_from_cart/<name>` | POST | Remove item from cart |
| `/buy` | POST | Checkout page |
| `/confirm_purchase` | POST | Complete purchase |

## Customization

### Styling
Modify `static/styles/styles.css` to customize the appearance:
- Colors and themes
- Layout and spacing
- Typography
- Animations and effects

### Templates
Edit HTML templates in the `templates/` directory:
- `index.html` - Homepage layout
- `product.html` - Product page design
- `cart.html` - Cart interface
- `checkout.html` - Checkout process

## Deployment

### Production Considerations
1. Set `debug=False` in production
2. Use a proper WSGI server (Gunicorn, uWSGI)
3. Set up environment variables for configuration
4. Implement proper session management
5. Add security headers and CSRF protection

### Environment Variables
Consider using environment variables for:
- `SECRET_KEY`
- `DATABASE_URL`
- `UPLOAD_FOLDER`

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## Roadmap

### Completed Features
- ✅ Product catalog and display
- ✅ Shopping cart functionality
- ✅ Search and filtering
- ✅ Basic checkout process
- ✅ Stock management

### Upcoming Features
- 🔄 Payment method integration (Stripe, PayPal)
- 🔄 User authentication and profiles
- 🔄 Order history and tracking
- 🔄 Product categories and filters
- 🔄 Admin dashboard
- 🔄 Email notifications
- 🔄 Product reviews and ratings
- 🔄 Wishlist functionality

## License

This project is open source and available under the [MIT License](LICENSE.txt).

## Support

For questions or issues, please:
1. Check the existing issues
2. Create a new issue with detailed information
3. Provide steps to reproduce any bugs

---

**Made with ❤️ by Om Goyal**