Some of the stuff I built:

---

#### ☸️ Ved – Full Stack Mock Website {#projects-ved}

_Postgres, React, CSS, Mistral API_ | ([Source](https://github.com/fringewidth/ved) | [Live](https://ved-one.vercel.app))

A site for research collaboration.

- Has search, auth, clean styling.
- Wired up Postgres with heavy joins and used generative AI to make synthetic data.
- Hacked around a super rate-limited LLM with exponential backoff (this was cool in early 2024).

[I mean you should see the joins](https://pastes.io/ved-user-page-view).

There's also a [cool YouTube demo](https://www.youtube.com/watch?v=FsQshAGo5vU).

---

#### 🌍 State of the World – Climate Change Visualizer {#projects-sotw}

_Azure, MERN stack, Three.js, Cosmos DB_ | ([Source](https://github.com/fringewidth/stateoftheworld) | [Live](https:/stateoftheworld.vercel.app))

Visualizes climate data and news for major economies.

- 3D globe with Three.js and a Node backend that caches data from Cosmos DB.
- Visualizes country-specific temperature changes, CO2, and general sentiment.
- All of this is updated every month with serverless.
- Used cloud AI trained on a custom dataset for estimating if news reported that month was good or bad for climate change.
- The custom dataset was downloaded more than 600 times on [Kaggle](https://kaggle.com/datasets/fringewidth/climate-change-news).

The backend API is also open source.
[Here's all the important climate change data for Jan 2024.](https://sotw.azurewebsites.net/months/1/2024)

---

#### 🐦‍⬛ Raven - Dimensionality Reduction Algorithm {#projects-raven}

_Graph theory, data analysis_ | ([Source](https://github.com/fringewidth/raven))

- Feature selection algorithm based on graph theory.
- Upto 70% reduction in bloated datasets.
- 40 lines of code (minus docstrings and empty lines).
- My proudest creation.

[There's an unfinished preprint on this](https://drive.google.com/file/d/1D6dzpmQe6o1U1X3-4uvdHB287tvvCE2a/view?usp=sharing). There's ablation, mathematical proof on why it works, few case studies, everything. One day I will find the time to seek its publication.

---

#### 🕸️ Arachnid – Web Scraping Chrome Extension {#projects-arachnid}

_DOM tree, React_ | ([Source](https://github.com/dragn0id/arachnid))

- Chrome extension that grabs correlated elements on a page in one click.
- Tested it on Amazon, Google Search, BigBasket, NDTV, India Today.
- This was a group project. My contribution was mostly designing the actual scraping algorithm, [selectData.js](https://github.com/dragn0id/arachnid/blob/main/src/components/customComponents/utils/selectData.js) and [ScrapeData.js](https://github.com/dragn0id/arachnid/blob/main/src/components/customComponents/utils/ScrapeData.js).
- Built this after training the classifier for [State of the World](#projects-sotw) because writing custom scrapers for each website was a pain.

---

#### 📈 JFit – Empirical Complexity Guesser {#projects-jfit}

_Java, Python, SciPy, JUnit_ | ([Source](https://github.com/fringewidth/jfit2))

- It takes in array functions.
- Spits out their complexity.
- First coding project.

[Here's the result for bubble sort.](https://github.com/user-attachments/assets/23b4800c-b457-46a1-bdce-e7b3040914e8)

[Also ported it to C++](https://github.com/fringewidth/cppFit).

---

#### 📑 This Website! {#projects-portfolio}

_HTML, CSS, jQuery_

- Wrote a tiny HTML+jQuery script that turns interlinked MD files into a full website. You can find this page's source [here](https://github.com/fringewidth/fringewidth.github.io/blob/main/projects.md), and the full repo [here](https://github.com/fringewidth/fringewidth.github.io).
- Yes, there are existing solutions that do this, but this one has a data footprint of 150kb and 60% of that is jQuery :)
- Also hacking together your website from scratch is very fun.

After building grandiose websites, you tend to admire the simplicity of the early internet.

Thanks to [Marked](https://marked.js.org/), there's only about 80 lines of HTML, most of it is for this footer ⬇️.
