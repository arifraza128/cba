import './ProductCards.css';

const products = [
  {
    id: 1,
    name: 'iPhone 16',
    price: 79999,
    rating: 4.8,
    image: 'https://via.placeholder.com/250',
  },
  {
    id: 2,
    name: 'MacBook Air',
    price: 99999,
    rating: 4.7,
    image: 'https://via.placeholder.com/250',
  },
  {
    id: 3,
    name: 'Sony Headphones',
    price: 19999,
    rating: 4.5,
    image: 'https://via.placeholder.com/250',
  },
  {
    id: 4,
    name: 'Samsung Galaxy',
    price: 69999,
    rating: 4.6,
    image: 'https://via.placeholder.com/250',
  },
];

function ProductCards() {
  return (
    <div className="products">
      {products.map((product) => (
        <div className="product-card" key={product.id}>
          <img src={product.image} alt={product.name} />

          <h2>{product.name}</h2>
          <p>₹{product.price}</p>
          <p>⭐ {product.rating}</p>

          <button>Buy Now</button>
        </div>
      ))}
    </div>
  );
}

export default ProductCards;
