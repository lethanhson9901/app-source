import { useState, useEffect } from 'react';
import { Plus, Loader } from 'lucide-react';

export default function ItemsManager() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');

  const fetchItems = async () => {
    try {
      const response = await fetch('/api/v1/items', {
        headers: {
          'X-API-Key': 'dev-secret-key'
        }
      });
      const data = await response.json();
      setItems(data);
    } catch (error) {
      console.error('Error fetching items:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchItems();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('/api/v1/items', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-API-Key': 'dev-secret-key'
        },
        body: JSON.stringify({
          name,
          description
        })
      });
      if (response.ok) {
        setName('');
        setDescription('');
        fetchItems();
      }
    } catch (error) {
      console.error('Error creating item:', error);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <Loader className="w-8 h-8 animate-spin text-blue-500" />
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-8">Item Manager</h1>

      <form onSubmit={handleSubmit} className="mb-8 space-y-4">
        <div>
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="Item name"
            className="w-full p-2 border rounded focus:ring-2 focus:ring-blue-500 outline-none"
            required
          />
        </div>
        <div>
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Description"
            className="w-full p-2 border rounded focus:ring-2 focus:ring-blue-500 outline-none"
            rows="3"
          />
        </div>
        <button
          type="submit"
          className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 flex items-center gap-2"
        >
          <Plus className="w-4 h-4" />
          Add Item
        </button>
      </form>

      <div className="space-y-4">
        {items.map((item) => (
          <div key={item.id} className="border rounded p-4 hover:shadow-md transition-shadow">
            <h2 className="text-xl font-semibold">{item.name}</h2>
            <p className="text-gray-600 mt-2">{item.description}</p>
            <div className="mt-2 text-sm text-gray-500">
              Created: {new Date(item.created_at).toLocaleString()}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
