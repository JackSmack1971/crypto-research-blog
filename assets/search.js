(() => {
  const form = document.querySelector("[data-search-form]");
  const grid = document.querySelector("[data-archive-grid]");
  if (!(form instanceof HTMLFormElement) || !(grid instanceof HTMLElement)) return;

  const cards = [...grid.querySelectorAll(".entry")];
  const featured = document.querySelector("[data-featured-search]");
  const status = document.querySelector("[data-search-status]");
  const count = document.querySelector("[data-result-count]");
  const empty = document.querySelector("[data-empty-state]");
  const search = form.elements.namedItem("q");
  const topic = form.elements.namedItem("topic");
  const researchType = form.elements.namedItem("research_type");
  if (!(search instanceof HTMLInputElement) || !(topic instanceof HTMLSelectElement) || !(researchType instanceof HTMLSelectElement)) return;

  const normalize = (value) => value.toLocaleLowerCase().normalize("NFKD").replace(/[\u0300-\u036f]/g, "").replace(/[^a-z0-9]+/g, " ").trim();
  const params = new URLSearchParams(window.location.search);
  search.value = params.get("q") || "";
  topic.value = params.get("topic") || "";
  researchType.value = params.get("research_type") || "";

  let records = [...cards, ...(featured instanceof HTMLElement ? [featured] : [])].map((card) => {
    const title = card.querySelector("h2")?.textContent || "";
    const dek = card.querySelector(".dek")?.textContent || "";
    return {
      card,
      isFeatured: card === featured,
      slug: card.dataset.slug || "",
      title: normalize(title),
      dek: normalize(dek),
      topic: card.dataset.topic || "",
      researchType: card.dataset.researchType || "",
      assets: (card.dataset.assets || "").split(/\s+/).filter(Boolean).map(normalize),
      date: card.querySelector("time")?.getAttribute("datetime") || "",
    };
  });

  // The generated index is also useful to other future clients. Load it as the
  // canonical searchable data source while retaining server-rendered cards.
  fetch("search-index.json")
    .then((response) => response.ok ? response.json() : Promise.reject(new Error("search index unavailable")))
    .then((index) => {
      const bySlug = new Map(index.map((item) => [item.slug, item]));
      records = records.map((record) => {
        const item = bySlug.get(record.slug);
        if (!item) return record;
        return {
          ...record,
          title: normalize(item.title),
          dek: normalize(item.dek),
          topic: item.topic,
          researchType: item.research_type,
          assets: item.assets.map(normalize),
          date: item.date,
        };
      });
      update();
    })
    .catch(() => {});

  function score(record, query) {
    if (!query) return 0;
    if (record.assets.includes(query)) return 100;
    if (record.title.includes(query)) return 90;
    const words = query.split(" ").filter(Boolean);
    if (words.length && words.every((word) => record.title.includes(word))) return 60;
    if (normalize(record.topic).includes(query)) return 40;
    if (record.dek.includes(query)) return 20;
    return -1;
  }

  function update() {
    const query = normalize(search.value);
    const selectedTopic = topic.value;
    const selectedType = researchType.value;
    const matches = records
      .map((record) => ({ record, rank: score(record, query) }))
      .filter(({ record, rank }) => rank >= 0 && (!selectedTopic || record.topic === selectedTopic) && (!selectedType || record.researchType === selectedType))
      .sort((a, b) => query ? b.rank - a.rank || b.record.date.localeCompare(a.record.date) : b.record.date.localeCompare(a.record.date));
    const visible = new Set(matches.map(({ record }) => record.slug));
    for (const record of records) {
      record.card.hidden = !visible.has(record.slug);
    }
    for (const { record } of matches) {
      if (!record.isFeatured) grid.append(record.card);
    }
    const amount = matches.length;
    const label = `${amount} ${amount === 1 ? "investigation" : "investigations"}`;
    if (status) status.textContent = query || selectedTopic || selectedType ? `${label} match your search` : label;
    if (count) count.textContent = label;
    if (empty instanceof HTMLElement) empty.hidden = amount !== 0;
    const next = new URL(window.location.href);
    for (const [key, value] of [["q", search.value.trim()], ["topic", selectedTopic], ["research_type", selectedType]]) {
      if (value) next.searchParams.set(key, value);
      else next.searchParams.delete(key);
    }
    window.history.replaceState(null, "", next);
  }

  form.addEventListener("input", update);
  form.addEventListener("change", update);
  form.addEventListener("reset", () => requestAnimationFrame(update));
  update();
})();
