function searchBook() {
    const query = document.getElementById('searchBox').value;
    if (!query) return;
    
    fetch(`https://openlibrary.org/search.json?q=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            const resultsDiv = document.getElementById('searchResults');
            resultsDiv.innerHTML = '';
            data.docs.slice(0, 10).forEach(book => {
                const bookElement = document.createElement('div');
                bookElement.className = 'book';
                bookElement.innerHTML = `<h3>${book.title}</h3><p>Author: ${book.author_name?.join(', ') || 'Unknown'}</p>`;
                bookElement.onclick = () => window.open(`https://openlibrary.org${book.key}`, '_blank');
                resultsDiv.appendChild(bookElement);
            });
        })
        .catch(error => console.error('Error fetching data:', error));
}
