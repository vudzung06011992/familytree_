import f3 from './index_support.js'

fetch("./family_people_list.json").then(r => r.json()).then(data => {

  const store = f3.createStore({
      data,
      node_separation: 250,
      level_separation: 150
    }),
    svg = f3.createSvg(document.querySelector("#FamilyChart")),
    Card = f3.elements.Card({
      store,
      svg,
      card_dim: {w:220,h:70,text_x:75,text_y:15,img_w:0,img_h:0,img_x:0,img_y:0},
      card_display: [
                              d => `${d.data["first name"]} ${d.data["last name"]}`,
                              d => `${d.data["birthday"] || ''}`
                            ],
      mini_tree: true,
      link_break: false
    })

  store.setOnUpdate(props => f3.view(store.getTree(), svg, Card, props || {}))
  store.updateTree({initial: true})
})
