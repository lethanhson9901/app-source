function Notification({ type, message }) {
    const style = type === 'success'
        ? { bg: 'bg-green-50', border: 'border-green-200', text: 'text-green-600', icon: 'text-green-500' }
        : { bg: 'bg-red-50', border: 'border-red-200', text: 'text-red-600', icon: 'text-red-500' };

    return (
        <div className={`mb-6 p-4 ${style.bg} border ${style.border} rounded-xl`}>
            <div className="flex items-center">
                <svg className={`w-5 h-5 ${style.icon} mr-2`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    {type === 'success' ? (
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
                    ) : (
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    )}
                </svg>
                <p className={style.text}>{message}</p>
            </div>
        </div>
    );
}

function ItemCard({ item, onEdit, onDelete }) {
    return (
        <div className="bg-white rounded-xl p-6 shadow-lg hover:shadow-xl transition-all duration-300">
            <div className="flex justify-between items-start">
                <h2 className="text-xl font-semibold text-gray-900">{item.name}</h2>
                <div className="flex space-x-2">
                    <button
                        onClick={() => onEdit(item)}
                        className="p-2 text-blue-600 hover:bg-blue-50 rounded-full transition-colors"
                        title="Edit item"
                    >
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                        </svg>
                    </button>
                    <button
                        onClick={() => onDelete(item.id)}
                        className="p-2 text-red-600 hover:bg-red-50 rounded-full transition-colors"
                        title="Delete item"
                    >
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                        </svg>
                    </button>
                </div>
            </div>
            <div className="mt-4 flex items-center text-sm text-gray-500">
                <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                {new Date(item.created_at).toLocaleString()}
            </div>
        </div>
    );
}

function ItemsManager() {
    const [items, setItems] = React.useState([]);
    const [loading, setLoading] = React.useState(true);
    const [name, setName] = React.useState('');
    const [notification, setNotification] = React.useState(null);
    const [editingItem, setEditingItem] = React.useState(null);

    // Add polling interval reference
    const pollingInterval = React.useRef(null);

    const showNotification = (type, message) => {
        setNotification({ type, message });
        setTimeout(() => setNotification(null), 3000);
    };

    const fetchItems = async () => {
        try {
            const response = await fetch('/api/v1/items', {
                headers: { 'X-API-Key': 'dev-secret-key' }
            });
            if (!response.ok) throw new Error('Failed to fetch items');
            const data = await response.json();
            setItems(data);
        } catch (error) {
            console.error('Error fetching items:', error);
        } finally {
            setLoading(false);
        }
    };

    React.useEffect(() => {
        fetchItems(); // Initial fetch

        // Start polling every 2 seconds
        pollingInterval.current = setInterval(fetchItems, 2000);

        // Cleanup when component unmounts
        return () => {
            if (pollingInterval.current) {
                clearInterval(pollingInterval.current);
            }
        };
    }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        try {
            const url = editingItem ? `/api/v1/items/${editingItem.id}` : '/api/v1/items';
            const method = editingItem ? 'PUT' : 'POST';

            const response = await fetch(url, {
                method,
                headers: {
                    'Content-Type': 'application/json',
                    'X-API-Key': 'dev-secret-key'
                },
                body: JSON.stringify({ name })
            });

            if (!response.ok) {
                throw new Error(editingItem ? 'Failed to update item' : 'Failed to create item');
            }

            setName('');
            setEditingItem(null);
            showNotification('success', editingItem ? 'Item updated successfully!' : 'Item added successfully!');
            await fetchItems(); // Immediate fetch after update
        } catch (error) {
            showNotification('error', error.message);
        } finally {
            setLoading(false);
        }
    };

    const handleEdit = (item) => {
        setEditingItem(item);
        setName(item.name);
        window.scrollTo({ top: 0, behavior: 'smooth' });
    };

    const handleDelete = async (itemId) => {
        if (!confirm('Are you sure you want to delete this item?')) return;

        try {
            const response = await fetch(`/api/v1/items/${itemId}`, {
                method: 'DELETE',
                headers: { 'X-API-Key': 'dev-secret-key' }
            });

            if (!response.ok) {
                throw new Error('Failed to delete item');
            }

            showNotification('success', 'Item deleted successfully!');
            await fetchItems(); // Immediate fetch after deletion
        } catch (error) {
            showNotification('error', error.message);
        }
    };

    const handleCancel = () => {
        setEditingItem(null);
        setName('');
    };

    return (
        <div className="min-h-screen py-12 px-4 sm:px-6">
            <div className="max-w-5xl mx-auto">
                <div className="text-center mb-12">
                    <h1 className="text-4xl font-bold gradient-text mb-2">Item Manager 123</h1>
                </div>

                <div className="glassmorphism rounded-2xl p-8 mb-12">
                    {notification && (
                        <Notification type={notification.type} message={notification.message} />
                    )}

                    <form onSubmit={handleSubmit} className="space-y-6">
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2" htmlFor="name">
                                Item Name
                            </label>
                            <input
                                id="name"
                                type="text"
                                value={name}
                                onChange={(e) => setName(e.target.value)}
                                placeholder="Enter item name"
                                className="w-full px-4 py-3 rounded-xl border border-gray-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-colors"
                                required
                            />
                        </div>
                        <div className="flex space-x-4">
                            <button
                                type="submit"
                                disabled={loading}
                                className={`
                                    flex-1 py-3 px-6 rounded-xl text-white font-medium
                                    ${loading ? 'bg-gray-400' : 'bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700'}
                                    transform transition-all duration-300 hover:scale-[1.02]
                                    focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500
                                    disabled:opacity-50 disabled:cursor-not-allowed
                                `}
                            >
                                {loading ? (
                                    <div className="flex items-center justify-center">
                                        <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
                                        Processing...
                                    </div>
                                ) : (editingItem ? 'Update Item' : 'Add Item')}
                            </button>
                            {editingItem && (
                                <button
                                    type="button"
                                    onClick={handleCancel}
                                    className="px-6 py-3 border border-gray-300 rounded-xl text-gray-700 hover:bg-gray-50 transition-colors"
                                >
                                    Cancel
                                </button>
                            )}
                        </div>
                    </form>
                </div>

                <div className="space-y-6">
                    {loading && !items.length ? (
                        <div className="flex flex-col items-center justify-center py-12">
                            <div className="w-12 h-12 border-4 border-indigo-500 border-t-transparent rounded-full animate-spin mb-4"></div>
                            <p className="text-gray-500">Loading items...</p>
                        </div>
                    ) : !items.length ? (
                        <div className="text-center py-12 bg-white rounded-xl shadow-lg">
                            <svg className="w-16 h-16 mx-auto text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
                            </svg>
                            <p className="text-xl font-medium text-gray-600">No items yet</p>
                            <p className="text-gray-500 mt-2">Add your first item above!</p>
                        </div>
                    ) : (
                        <div className="grid gap-6 md:grid-cols-2">
                            {items.map((item) => (
                                <ItemCard
                                    key={item.id}
                                    item={item}
                                    onEdit={handleEdit}
                                    onDelete={handleDelete}
                                />
                            ))}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
