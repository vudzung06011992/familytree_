import d3 from "../d3.js"
import f3 from "../index.js"
import {processCardDisplay} from "./utils.js"
import {pathToMain} from "../CalculateTree/createLinks.js"

CardHtmlWrapper.is_html = true
export default function CardHtmlWrapper(...args) { return new CardHtml(...args) }

CardHtml.prototype.is_html = true
function CardHtml(cont, store) {
  this.cont = cont
  this.store = store
  this.getCard = null
  this.card_display = [d => `${d.data["first name"]} ${d.data["last name"]}`]
  this.cardImageField = 'avatar'
  this.onCardClick = this.onCardClickDefault
  this.style = 'default'
  this.mini_tree = false
  this.onCardUpdate = null
  this.card_dim = {}
  this.cardInnerHtmlCreator = null

  this.init()

  return this
}

CardHtml.prototype.init = function() {
  this.svg = this.cont.querySelector('svg.main_svg')

  this.getCard = () => f3.elements.CardHtml({
    store: this.store,
    card_display: this.card_display,
    cardImageField: this.cardImageField,
    defaultPersonIcon: this.defaultPersonIcon,
    onCardClick: this.onCardClick,
    style: this.style,
    mini_tree: this.mini_tree,
    onCardUpdate: this.onCardUpdate,
    card_dim: this.card_dim,
    empty_card_label: this.store.state.single_parent_empty_card_label,
    cardInnerHtmlCreator: this.cardInnerHtmlCreator,
    duplicate_branch_toggle: this.store.state.duplicate_branch_toggle,
    onCardMouseenter: this.onCardMouseenter ? this.onCardMouseenter.bind(this) : null,
    onCardMouseleave: this.onCardMouseleave ? this.onCardMouseleave.bind(this) : null
  })
}

CardHtml.prototype.setCardDisplay = function(card_display) {
  this.card_display = processCardDisplay(card_display)

  return this
}

CardHtml.prototype.setCardImageField = function(cardImageField) {
  this.cardImageField = cardImageField
  return this
}

CardHtml.prototype.setDefaultPersonIcon = function(defaultPersonIcon) {
  this.defaultPersonIcon = defaultPersonIcon
  return this
}

CardHtml.prototype.setOnCardClick = function(onCardClick) {
  this.onCardClick = onCardClick
  return this
}

CardHtml.prototype.onCardClickDefault = function(e, d) {
  this.store.updateMainId(d.data.id)
  this.store.updateTree({})
  
  // Center the tree after update
  setTimeout(() => {
    this.centerTree()
  }, 100) // Small delay to ensure tree has updated
}

CardHtml.prototype.centerTree = function() {
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

CardHtml.prototype.setStyle = function(style) {
  this.style = style
  return this
}

CardHtml.prototype.setMiniTree = function(mini_tree) {
  this.mini_tree = mini_tree

  return this
}

CardHtml.prototype.setOnCardUpdate = function(onCardUpdate) {
  this.onCardUpdate = onCardUpdate
  return this
}

CardHtml.prototype.setCardDim = function(card_dim) {
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

  return this
}

CardHtml.prototype.resetCardDim = function() {
  this.card_dim = {}
  return this
}

CardHtml.prototype.setCardInnerHtmlCreator = function(cardInnerHtmlCreator) {
  this.cardInnerHtmlCreator = cardInnerHtmlCreator

  return this
}

CardHtml.prototype.setOnHoverPathToMain = function() {
  this.onCardMouseenter = this.onEnterPathToMain.bind(this)
  this.onCardMouseleave = this.onLeavePathToMain.bind(this)
  return this
}

CardHtml.prototype.unsetOnHoverPathToMain = function() {
  this.onCardMouseenter = null
  this.onCardMouseleave = null
  return this
}

CardHtml.prototype.onEnterPathToMain = function(e, datum) {
  this.to_transition = datum.data.id
  const main_datum = this.store.getTreeMainDatum()
  const cards = d3.select(this.cont).select('div.cards_view').selectAll('.card_cont')
  const links = d3.select(this.cont).select('svg.main_svg .links_view').selectAll('.link')
  const [cards_node_to_main, links_node_to_main] = pathToMain(cards, links, datum, main_datum)
  cards_node_to_main.forEach(d => {
    const delay = Math.abs(datum.depth - d.card.depth) * 200
    d3.select(d.node.querySelector('div.card-inner'))
      .transition().duration(0).delay(delay)
      .on('end', () => this.to_transition === datum.data.id && d3.select(d.node.querySelector('div.card-inner')).classed('f3-path-to-main', true))
  })
  links_node_to_main.forEach(d => {
    const delay = Math.abs(datum.depth - d.link.depth) * 200
    d3.select(d.node)
      .transition().duration(0).delay(delay)
      .on('end', () => this.to_transition === datum.data.id && d3.select(d.node).classed('f3-path-to-main', true))
  })

  return this
}

CardHtml.prototype.onLeavePathToMain = function(e, d) {
  this.to_transition = false
  d3.select(this.cont).select('div.cards_view').selectAll('div.card-inner').classed('f3-path-to-main', false)
  d3.select(this.cont).select('svg.main_svg .links_view').selectAll('.link').classed('f3-path-to-main', false)

  return this
}
