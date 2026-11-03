(() => {
  const form = document.querySelector("[data-search-form]");
  const grid = document.querySelector("[data-archive-grid]");
  const featured = document.querySelector("[data-featured-search]");
  const featureSlot = document.querySelector("[data-feature-slot]");
  if (!(form instanceof HTMLFormElement) || !(grid instanceof HTMLElement)) return;

  const cards = [...grid.querySelectorAll(".entry")];
  const status = document.querySelector("[data-search-status]");
  const count = document.querySelector("[data-result-count]");
  const empty = document.querySelector("[data-empty-state]");
  const search = form.elements.namedItem("q");
  const topic = form.elements.namedItem("topic");
  const researchType = form.elements.namedItem("research_type");
  if (!(search instanceof HTMLInputElement) || !(topic instanceof HTMLSelectElement) || !(researchType instanceof HTMLSelectElement)) return;

  const normalize = (value) => value.toLocaleLowerCase().normalize("NFKD").replace(/[\u0300-\u036f]/g, "").replace(/[^a-z0-9]+/g, " ").trim();
  const tokens = (value) => normalize(value).split(/\s+/).filter(Boolean);
  const params = new URLSearchParams(window.location.search);
  search.value = params.get("q") || "";
  topic.value = params.get("topic") || "";
  researchType.value = params.get("research_type") || "";

  const records = [...cards, ...(featured instanceof HTMLElement ? [featured] : [])].map((card) => {
    const title = card.querySelector("h2")?.textContent || "";
    const dek = card.querySelector(".dek")?.textContent || "";
    return {
      card,
      isFeatured: card === featured,
      slug: card.dataset.slug || "",
      title: tokens(title),
      dek: tokens(dek),
      topic: card.dataset.topic || "",
      topicWords: tokens(card.dataset.topic || ""),
      researchType: card.dataset.researchType || "",
      assets: tokens(card.dataset.assets || ""),
      date: card.querySelector("time")?.getAttribute("datetime") || "",
    };
  });

  function score(record, query) {
    if (!query.length) return 0;
    let total = 0;
    for (const term of query) {
      const exactAsset = record.assets.includes(term);
      const assetPrefix = record.assets.some((word) => word.startsWith(term));
      const exactTitle = record.title.includes(term);
      const titlePrefix = record.title.some((word) => word.startsWith(term));
      const exactTopic = record.topicWords.includes(term);
      const topicPrefix = record.topicWords.some((word) => word.startsWith(term));
      const exactDek = record.dek.includes(term);
      const dekPrefix = record.dek.some((word) => word.startsWith(term));
      const rank = exactAsset ? 140
        : assetPrefix ? 120
          : exactTitle ? 100
            : titlePrefix ? 80
              : exactTopic ? 70
                : topicPrefix ? 60
                  : exactDek ? 40
                    : dekPrefix ? 30
                      : 0;
      if (!rank) return -1;
      total += rank;
    }
    return total;
  }

  function update() {
    const query = tokens(search.value);
    const selectedTopic = topic.value;
    const selectedType = researchType.value;
    const filtering = query.length > 0 || Boolean(selectedTopic) || Boolean(selectedType);
    const matches = records
      .map((record) => ({ record, rank: score(record, query) }))
      .filter(({ record, rank }) => rank >= 0 && (!selectedTopic || record.topic === selectedTopic) && (!selectedType || record.researchType === selectedType))
      .sort((a, b) => filtering ? b.rank - a.rank || b.record.date.localeCompare(a.record.date) : b.record.date.localeCompare(a.record.date));
    const visible = new Set(matches.map(({ record }) => record.slug));
    for (const record of records) record.card.hidden = !visible.has(record.slug);

    const featuredMatch = matches.some(({ record }) => record.isFeatured);
    if (featured instanceof HTMLElement) {
      if (filtering && featuredMatch) {
        featured.classList.add("entry", "featured-result");
        featured.hidden = false;
      } else {
        featured.classList.remove("entry", "featured-result");
        if (featureSlot instanceof HTMLElement) featureSlot.after(featured);
        featured.hidden = filtering;
      }
    }

    for (const { record } of matches) {
      if (record.isFeatured) {
        if (filtering && featuredMatch) grid.append(record.card);
      } else {
        grid.append(record.card);
      }
    }

    const amount = matches.length;
    const label = `${amount} ${amount === 1 ? "investigation" : "investigations"}`;
    if (status) status.textContent = filtering ? `${label} found` : label;
    if (count) count.textContent = label;
    if (empty instanceof HTMLElement) empty.hidden = amount !== 0;

    const next = new URL(window.location.href);
    for (const [key, value] of [["q", search.value.trim()], ["topic", selectedTopic], ["research_type", selectedType]]) {
      if (value) next.searchParams.set(key, value);
      else next.searchParams.delete(key);
    }
    window.history.replaceState(null, "", next);
  }

  document.body.classList.add("js-ready");
  form.addEventListener("input", update);
  form.addEventListener("change", update);
  form.addEventListener("reset", () => requestAnimationFrame(update));
  update();
})();
