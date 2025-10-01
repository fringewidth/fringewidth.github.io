hi. i'm hrishik sai bojnal. i am interested in consciousness. find me at:

- 🐙 [github](https://github.com/fringewidth)
- 🐦 [twitter](https://x.com/saibojnal)
- 🐵 [monkeytype](https://monkeytype.com/profile/fringewidth)
- 🌐 [everywhere else](https://www.google.com/search?q=hrishik+sai+bojnal)

<h2 id="news-heading"><a href="news.md">News:</a></h2>

<table id="homepage_news" class="newstable"></table>
<button id="news_load_btn" onclick="loadMore()">...load more</button>

<script>
let newsDisplayCount = null
async function initalizeNews() {
fetch("config.json")
    .then(res => res.json())
    .then(config => {
        newsDisplayCount = config.news.homepageLimit 
        populateNews("homepage_news", newsDisplayCount)
    })
}
initalizeNews()
function loadMore() {
    if(newsDisplayCount) {
        newsDisplayCount += 5;
        populateNews("homepage_news", newsDisplayCount)
    }
}
</script>
