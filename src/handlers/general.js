import d3 from "../d3.js"

export function manualZoom({amount, svg, transition_time=500}) {
  const el_listener = svg.__zoomObj ? svg : svg.parentNode  // if we need listener for svg and html, we will use parent node
  const zoom = el_listener.__zoomObj
  
  // Get the center point of the container
  const rect = el_listener.getBoundingClientRect();
  const center = [rect.width / 2, rect.height / 2];
  const currentTransform = d3.zoomTransform(el_listener);
  
  // Calculate new transform that keeps the center point fixed
  const newK = Math.max(0.5, Math.min(2, currentTransform.k * amount)); // Giới hạn zoom từ 0.5x đến 2x
  const scale_factor = newK / currentTransform.k;
  const newX = center[0] - (center[0] - currentTransform.x) * scale_factor;
  const newY = center[1] - (center[1] - currentTransform.y) * scale_factor;
  
  const newTransform = d3.zoomIdentity.translate(newX, newY).scale(newK);
  
  d3.select(el_listener).transition().duration(transition_time || 0).delay(transition_time ? 100 : 0)
    .call(zoom.transform, newTransform);
}

export function getCurrentZoom(svg) {
  const el_listener = svg.__zoomObj ? svg : svg.parentNode
  const currentTransform = d3.zoomTransform(el_listener)
  return currentTransform
}

export function zoomTo(svg, zoom_level) {
  const el_listener = svg.__zoomObj ? svg : svg.parentNode
  const currentTransform = d3.zoomTransform(el_listener)
  manualZoom({amount: zoom_level / currentTransform.k, svg})
}

export function isAllRelativeDisplayed(d, data) {
  const r = d.data.rels,
    all_rels = [r.father, r.mother, ...(r.spouses || []), ...(r.children || [])].filter(v => v)
  return all_rels.every(rel_id => data.some(d => d.data.id === rel_id))
}