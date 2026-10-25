function embedChart(id, file) {
  const el = document.getElementById(id);
  if (!el) {
    console.error(`Missing chart container: ${id}`);
    return;
  }
  vegaEmbed(el, file, { actions: false, renderer: "canvas" }).catch(err => {
    console.error(`Could not load ${file}`, err);
    el.innerHTML = `<p class="chart-error">This chart could not load. Check the browser console and data paths.</p>`;
  });
}

document.addEventListener("DOMContentLoaded", () => {
  const charts = [
    ["map_choropleth", "map_choropleth.vega.json"],
    ["map_dot", "map_dot.vega.json"],
    ["map_symbol", "map_symbol.vega.json"],
    ["map_layered", "map_layered.vega.json"],
    ["operator_bar", "operator_bar.vega.json"],
    ["market_day_bar", "market_day_bar.vega.json"],
    ["arc_chart", "arc_chart.vega.json"],
    ["bar_chart", "bar_chart.vega.json"],
    ["heatmap", "heatmap.vega.json"],
    ["line_chart", "line_chart.vega.json"],
    ["area_chart", "area_chart.vega.json"],
    ["scatter_plot", "scatter_plot.vega.json"],
    ["calendar_heatmap", "calendar_heatmap.vega.json"],
    ["start_time_dot", "start_time_dot.vega.json"]
  ];
  charts.forEach(([id, file]) => embedChart(id, file));
});