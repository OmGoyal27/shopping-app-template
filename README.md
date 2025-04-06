# Shopping app template

Hello everyone! Today I have made a shopping app template! All you have to do is run the `app.py` file and open <a href="http://localhost:5000">this link</a> to view the site.

# Adding products

To add new products, add a new folder in the `Products` directory.

For the naming of the folder, name it to anything you like, but remember, the link to you product will be the name of your directory.

And when it comes to the details of the product, make a new JSON file named `details.json` in that directory. The contents of the JSON file should be something like this:

```json
{
    "name": "Product name",
    "price": 100,
    "description": "Product description",
    "images": [
        "assets/image.png",
        "assets/image.png",
        "assets/image.png"
    ],
    "stock": 10
}
```

# To-Dos

- Make the buy button redirect to a page, which is posted with the list of items.

- Make a cart feature.