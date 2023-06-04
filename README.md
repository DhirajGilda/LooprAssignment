# LooprAssignment
# User Cart API

This project implements a user cart API with JWT-based authentication using Python and FastAPI. It allows users to register, login, and manage their shopping carts by adding, updating, and deleting products.

## Features

- User registration and login with password hashing
- JWT-based authentication for protected routes
- Adding, updating, and deleting products in the user's cart
- Aggregated cart information including total price and total quantity
- Integration with a coupon code functionality for applying discounts

## Requirements

- Python
- FastAPI
- Uvicorn (for running the server)
- PyJWT
- Passlib
- Pydantic

## Installation

1. Clone the repository:

Replace `<repository-url>` with the URL of this GitHub repository.

2. Install the required dependencies using pip:


3. Start the server:

The server should now be running on http://localhost:8000.

## API Endpoints

- `POST /users/register`: Register a new user.
- `POST /users/login`: Login with username and password to obtain an access token.
- `GET /users/me`: Get the current user's information.
- `POST /cart/add`: Add a product to the user's cart.

**Note**: Please refer to the code for additional API endpoints related to managing the cart.

## Authentication

This API uses JWT-based authentication. To access protected routes, include the JWT access token in the `Authorization` header of your requests:
Replace `<access-token>` with the access token obtained from the login endpoint.

## Data Storage

- User data is stored in a JSON file (`data/users.json`).
- Product data is stored in a JSON file (`data/products.json`).
- Cart data is stored in separate JSON files for each user (`data/cart_<username>.json`).

## Contributing

Contributions to this project are welcome. Feel free to open issues and submit pull requests to suggest improvements or add new features.

## License

This project is licensed under the [MIT License](LICENSE).
