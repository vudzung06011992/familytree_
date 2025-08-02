import d3 from "../../d3.js";

export default function Link({d, entering, exiting}) {
  const path = createPath(d, entering, exiting);

  return {template: (`
    <path d="${path}" fill="none" stroke="#fff" stroke-linecap="square" stroke-linejoin="miter" />
  `)}
}

export function createPath(d, is_) {
  const path_data = is_ ? d._d() : d.d
  
  if (!path_data || path_data.length === 0) return ""
  
  // Use D3 line with linear interpolation (no curves)
  const line = d3.line().curve(d3.curveLinear)
  return line(path_data)
}