some of the stuff i built:

---

#### ☸️ Ved – full stack mock website {#projects-ved}

_postgres, react, css, mistral api_ | ([Source](https://github.com/fringewidth/ved) | [Live](https://ved-one.vercel.app))

a site for research collaboration.

- has search, auth, clean styling.
- wired up postgres with heavy joins and used generative ai to make synthetic data.
- hacked around a super rate-limited llm with exponential backoff (this was cool in early 2024).

[i mean you should see the joins](https://pastes.io/ved-user-page-view).

there's also a [cool youtube demo](https://www.youtube.com/watch?v=FsQshAGo5vU)

---

#### 🌍 State of the World – climate change visualizer {#projects-sotw}

_azure, mern stack, three.js, cosmos db_ | ([Source](https://github.com/fringewidth/stateoftheworld) | [Live](https:/stateoftheworld.vercel.app))

visualizes climate data and news for major economies.

- 3d globe with three.js and a node backend that caches data from cosmos db.
- visualizes country-specific temperature changes, co2, and general sentiment.
- all of this is updated every month with serverless.
- used cloud AI trained on a custom dataset for estimating if news reported that month was good or bad for climate change.
- the custom dataset was downloaded more than 600 times on [kaggle](https://kaggle.com/datasets/fringewidth/climate-change-news)

the backend API is also open source.
[here's all the important climate change data for Jan 2024.](https://sotw.azurewebsites.net/months/1/2024)

---

#### Raven - dimensionality reduction algorithm {#projects-raven}

_graph theory, data analysis_ | ([Source](https://github.com/fringewidth/raven))

- feature selection algorithm based on graph theory.
- upto 70% reduction in bloated datasets.
- 40 lines of code (minus docstrings and empty lines)
- my proudest creation.

[there's an unfinished preprint on this](https://drive.google.com/file/d/1D6dzpmQe6o1U1X3-4uvdHB287tvvCE2a/view?usp=sharing). there's ablation, mathematical proof on why it works, few case studies, everything. one day i will find the time to seek its publication.

---

#### 🕸️ Arachnid – web scraping chrome extension {#projects-arachnid}

_dom tree, react_ |  ([Source](https://github.com/dragn0id/arachnid))

- chrome extension that grabs correlated elements on a page in one click.
- tested it on amazon, google search, bigbasket, ndtv, india today.
- this was a group project. my contribution was mostly designing the actual scraping algorithm, [selectData.js](https://github.com/dragn0id/arachnid/blob/main/src/components/customComponents/utils/selectData.js) and [ScrapeData.js](https://github.com/dragn0id/arachnid/blob/main/src/components/customComponents/utils/ScrapeData.js).
- built this after training the classifier for [state of the world](#projects-sotw). writing custom scrapers for each website was a pain.

---

#### 📈 JFit – empirical complexity guesser {#projects-jfit}

_java, python, scipy, junit_ | ([Source](https://github.com/fringewidth/jfit2))

- it takes in array functions.
- spits out their complexity.
- first coding project.

[here's the result for bubble sort.](https://github.com/user-attachments/assets/23b4800c-b457-46a1-bdce-e7b3040914e8)

[also ported it to cpp](https://github.com/fringewidth/cppFit)

---

#### 📑 This website! {#projects-portfolio}

_html, css, jquery_

wrote a tiny html+jquery script that turns interlinked md files into a full website. you can find this page's source [here](https://github.com/fringewidth/fringewidth.github.io/blob/main/projects.md), and the full repo [here](https://github.com/fringewidth/fringewidth.github.io)

after building grandiose websites, you tend to admire the simplicity of the early internet.

thanks to [Marked](https://marked.js.org/), there's only about 80 lines of HTML, most of it is for this footer ⬇️.
