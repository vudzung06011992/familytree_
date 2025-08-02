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
      card_dim: {w:220,h:80,text_x:110,text_y:15,img_w:0,img_h:0,img_x:0,img_y:0},
      card_display: [
                              d => {
                                const fullName = `${d.data["first name"] || ''} ${d.data["last name"] || ''}`.trim();
                                // If name is too long (> 15 characters), split into two lines
                                if (fullName.length > 15) {
                                  const words = fullName.split(' ');
                                  const mid = Math.ceil(words.length / 2);
                                  const firstLine = words.slice(0, mid).join(' ');
                                  const secondLine = words.slice(mid).join(' ');
                                  return `${firstLine}\n${secondLine}`;
                                }
                                return fullName;
                              },
                              d => `${d.data["birthday"] || ''}`
                            ],
      mini_tree: true,
      link_break: false
    })

  store.setOnUpdate(props => f3.view(store.getTree(), svg, Card, props || {}))
  store.updateTree({initial: true})
})
