hi. i'm hrishik sai bojnal. i am interested in consciousness. find me at:

- 🐙 [github](https://github.com/fringewidth)
- 🐦 [twitter](https://x.com/saibojnal)
- 🐵 [monkeytype](https://monkeytype.com/profile/fringewidth)
- 🌐 [everywhere else](https://www.google.com/search?q=hrishik+sai+bojnal)

<h2 id="news-heading"></h2>

<table id="homepage_news" class="newstable"></table>

<script>
populateNews("homepage_news", 5);

let newsDisplayCount = null;
let totalNewsLength = null;

async function initalizeNews() {
    newsDisplayCount = await fetch("config.json")
        .then(res => res.json())
        .then(config => config.news.homepageLimit)
    if(!totalNewsLength) {
        totalNewsLength = await fetch("news.json")
        .then(res => res.json())
    
        .then(newsArray => newsArray.length) 
    }
    const newsTable = document.getElementById('homepage_news');
    if (newsTable && newsDisplayCount < totalNewsLength) {
        const loadMoreBtn = document.createElement('button');
        const newsHeading = document.createElement('a');
        newsHeading.href = "news.md";
        newsHeading.textContent = "News:";

        loadMoreBtn.id = 'news_load_btn';
        loadMoreBtn.textContent = '...load more';
        loadMoreBtn.addEventListener('click', loadMore); 
        
        document.getElementById("news-heading").appendChild(newsHeading);
        newsTable.after(loadMoreBtn);
    }
    populateNews("homepage_news", newsDisplayCount);
}

function loadMore() {
    if (typeof newsDisplayCount === 'number') {
        newsDisplayCount += 5;
        populateNews("homepage_news", newsDisplayCount);
        if (newsDisplayCount >= totalNewsLength) {
            const loadMoreBtn = document.getElementById('news_load_btn');
            if (loadMoreBtn) {
            
                loadMoreBtn.remove(); 
            }
        }
    }
}

initalizeNews();
</script>
