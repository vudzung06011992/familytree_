import d3 from "../d3.js"
import f3 from "../index.js"
import {updateCardSvgDefs} from "../view/elements/Card.defs.js"
import {processCardDisplay} from "./utils.js"

CardSvgWrapper.is_html = false
export default function CardSvgWrapper(...args) { return new CardSvg(...args) }

function CardSvg(cont, store) {
  this.cont = cont
  this.store = store
  this.svg = null
  this.getCard = null
  this.card_dim = {w:220,h:70,text_x:75,text_y:15,img_w:60,img_h:60,img_x:5,img_y:5}
  this.card_display = [d => `${d.data["first name"]} ${d.data["last name"]}`]
  this.mini_tree = true
  this.link_break = false
  this.onCardClick = this.onCardClickDefault.bind(this)
  this.onCardUpdate = null

  this.init()

  return this
}

CardSvg.prototype.init = function() {
  this.svg = this.cont.querySelector('svg.main_svg')

  this.getCard = () => f3.elements.CardSvg({
    store: this.store,
    svg: this.svg,
    card_dim: this.card_dim,
    card_display: this.card_display,
    mini_tree: this.mini_tree,
    link_break: this.link_break,
    onCardClick: this.onCardClick,
    onCardUpdate: this.onCardUpdate
  })
}

CardSvg.prototype.setCardDisplay = function(card_display) {
  this.card_display = processCardDisplay(card_display)

  return this
}

CardSvg.prototype.setCardDim = function(card_dim) {
  if (typeof card_dim !== 'object') {
    console.error('card_dim must be an object')
    return this
  }
  for (let key in card_dim) {
    const val = card_dim[key]
    if (typeof val !== 'number' && typeof val !== 'boolean') {
      console.error(`card_dim.${key} must be a number or boolean`)
      return this
    }
    if (key === 'width') key = 'w'
    if (key === 'height') key = 'h'
    if (key === 'img_width') key = 'img_w'
    if (key === 'img_height') key = 'img_h'
    if (key === 'img_x') key = 'img_x'
    if (key === 'img_y') key = 'img_y'
    this.card_dim[key] = val
  }

  updateCardSvgDefs(this.svg, this.card_dim)

  return this
}

CardSvg.prototype.setOnCardUpdate = function(onCardUpdate) {
  this.onCardUpdate = onCardUpdate
  return this
}

CardSvg.prototype.setMiniTree = function(mini_tree) {
  this.mini_tree = mini_tree

  return this
}

CardSvg.prototype.setLinkBreak = function(link_break) {
  this.link_break = link_break

  return this
}

CardSvg.prototype.onCardClickDefault = function(e, d) {
  this.store.updateMainId(d.data.id)
  this.store.updateTree({})
  
  // Center the tree after update
  setTimeout(() => {
    this.centerTree()
  }, 100) // Small delay to ensure tree has updated
}

CardSvg.prototype.centerTree = function() {
  const svg = document.querySelector('#FamilyChart svg')
  if (!svg || !svg.__zoomObj) return
  
  const view = svg.querySelector('.view')
  if (!view) return
  
  // Get tree bounds
  const bbox = view.getBBox()
  if (bbox.width === 0 || bbox.height === 0) return
  
  // Get container dimensions
  const containerRect = svg.getBoundingClientRect()
  const containerWidth = containerRect.width
  const containerHeight = containerRect.height
  
  // Calculate scale to fit tree with some padding
  const padding = 50
  const scaleX = (containerWidth - padding * 2) / bbox.width
  const scaleY = (containerHeight - padding * 2) / bbox.height
  const scale = Math.min(scaleX, scaleY, 1) // Don't zoom in beyond 1x
  
  // Calculate center position
  const centerX = containerWidth / 2
  const centerY = containerHeight / 2
  const treeCenterX = bbox.x + bbox.width / 2
  const treeCenterY = bbox.y + bbox.height / 2
  
  // Calculate translation to center the tree
  const translateX = centerX - treeCenterX * scale
  const translateY = centerY - treeCenterY * scale
  
  // Apply transform
  const transform = d3.zoomIdentity.translate(translateX, translateY).scale(scale)
  d3.select(svg).transition().duration(500).call(svg.__zoomObj.transform, transform)
}

CardSvg.prototype.setOnCardClick = function(onCardClick) {
  this.onCardClick = onCardClick

  return this
}