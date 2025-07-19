import d3 from "../../d3.js"

import {calculateDelay} from "../view.js"


export default function linkSpouseText(svg, tree, props={}) {
  const links_data = []
  tree.data.forEach(d => {
    if (d._spouse && d.data.data.gender === 'F') links_data.push({nodes: [d, d._spouse], id: `${d.data.id}--${d._spouse.data.id}`})
    if (d.spouses) d.spouses.forEach(sp => links_data.push({nodes: [sp, d], id: `${sp.data.id}--${d.data.id}`}))
  })

  const link = d3.select(svg).select(".links_view").selectAll("g.link-text").data(links_data, d => d.id)
  const link_exit = link.exit()
  const link_enter = link.enter().append("g").attr("class", "link-text")
  const link_update = link_enter.merge(link)
  const spouseLineX = (sp1, sp2) => {
    if (sp1.spouse && sp1.data.data.gender === 'F') return sp1.x - props.node_separation/2
    else if (sp2.spouse && sp2.data.data.gender === 'M') return sp2.x + props.node_separation/2
    else return Math.min(sp1.x, sp2.x) + props.node_separation/2
  }

  link_exit.each(linkExit)
  link_enter.each(linkEnter)
  link_update.each(linkUpdate)

  function linkEnter(d) {
    const [sp1, sp2] = d.nodes
    const text_g = d3.select(this)
    text_g
      .attr('transform', `translate(${spouseLineX(sp1, sp2)}, ${sp1.y-3})`)
      .style('opacity', 0)

    text_g.append("text").style('font-size', '12px').style('fill', '#fff').style('text-anchor', 'middle')
  }

  function linkUpdate(d) {
    const [sp1, sp2] = d.nodes
    const text_g = d3.select(this)
    const delay = props.initial ? calculateDelay(tree, sp1, props.transition_time) : 0
    text_g.select('text').text(props.linkSpouseText(sp1, sp2))
    text_g.transition('text').duration(props.transition_time).delay(delay)
    .attr('transform', `translate(${spouseLineX(sp1, sp2)}, ${sp1.y-3})`)
    text_g.transition('text-op').duration(100).delay(delay + props.transition_time).style('opacity', 1)
  }

  function linkExit(d) {
    const text_g = d3.select(this);
    text_g.transition('text').duration(100).style('opacity', 0)
      .on("end", () => text_g.remove())
  }

}