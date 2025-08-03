import f3 from './index_support.js'

// Access d3 from global scope
const d3 = window.d3;

function createFamilyTree(data = null) {
  // Sử dụng data được truyền vào, hoặc từ global variable, hoặc từ file
  const getData = () => {
    if (data) return Promise.resolve(data);
    if (window.familyData) return Promise.resolve(window.familyData);
    // Fallback: thử load từ file (chỉ hoạt động local)
    return fetch("./family_people_list.json").then(r => r.json()).catch(() => []);
  };

  getData().then(familyData => {
    if (!familyData || familyData.length === 0) {
      console.warn('No family data available');
      return;
    }

    // Hook into family-chart zoom behavior and add constraints
    const originalCreateSvg = f3.createSvg;
    
    const store = f3.createStore({
        data: familyData,
        node_separation: 250,
        level_separation: 180,
        single_parent_empty_card: false
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
      });

    // Interactive features with zoom constraints  
    store.setOnUpdate(props => {
      console.log('Store updated, rendering view...');
      f3.view(store.getTree(), svg, Card, props || {});
      
      // Apply zoom constraints to the existing zoom behavior
      setTimeout(() => {
        const container = document.querySelector('#FamilyChart #f3Canvas');
        if (container && container.__zoomObj) {
          // Modify existing zoom behavior to add scale constraints
          const existingZoom = container.__zoomObj;
          
          // Set scale extent (zoom limits)
          existingZoom.scaleExtent([0.5, 2.0]);
          
          // Override zoom event handler to add zoom indicator
          const originalZoomFn = existingZoom.on('zoom');
          existingZoom.on('zoom', function(event) {
            // Call original zoom function first
            if (originalZoomFn) originalZoomFn.call(this, event);
            
            // Update zoom indicator
            const transform = event.transform;
            const scale = transform.k;
            const indicator = document.getElementById('zoom-indicator');
            
            if (indicator) {
              indicator.style.display = 'block';
              indicator.textContent = `Zoom: ${Math.round(scale * 100)}%`;
              
              if (scale <= 0.5) {
                indicator.textContent = 'Zoom: 50% (Min)';
                indicator.style.background = 'rgba(255, 100, 100, 0.9)';
              } else if (scale >= 2.0) {
                indicator.textContent = 'Zoom: 200% (Max)';
                indicator.style.background = 'rgba(255, 100, 100, 0.9)';
              } else {
                indicator.style.background = 'rgba(0, 0, 0, 0.7)';
              }
              
              clearTimeout(window.zoomTimeout);
              window.zoomTimeout = setTimeout(() => {
                indicator.style.display = 'none';
              }, 2000);
            }
          });
          
          console.log('Zoom constraints applied: 0.5x to 2.0x');
        }
      }, 100);
      
      // Bind click events after view update
      setTimeout(() => {
        // Try multiple selectors to find cards
        const cards = svg.selectAll('.card, .card-main, .person-card, [data-card]');
        console.log('Found cards:', cards.size());
        
        // Also check DOM elements
        const domCards = document.querySelectorAll('#FamilyChart .card, #FamilyChart rect, #FamilyChart g');
        console.log('DOM cards found:', domCards.length);
        
        cards.on('click', function(event, d) {
          console.log('D3 Card clicked:', d);
          event.stopPropagation();
          
          // Focus on clicked person - use proper data structure
          if (d && (d.id || d.data)) {
            const personId = d.id || d.data.id;
            console.log('Focusing on person:', personId);
            store.updateTree({tree_position: personId});
          }
        });
        
        // Add direct DOM event listeners as backup
        domCards.forEach((element, index) => {
          element.addEventListener('click', function(e) {
            console.log('DOM click handler fired for element', index);
            e.stopPropagation();
            
            // Try to get data from element
            const d3Data = d3.select(this).datum();
            console.log('Element data:', d3Data);
            
            if (d3Data && (d3Data.id || d3Data.data)) {
              const personId = d3Data.id || d3Data.data.id;
              store.updateTree({tree_position: personId});
            }
          });
        });
      }, 300);
    });
    
    // Initial render with full interactivity
    store.updateTree({initial: true});
  }).catch(err => {
    console.error('Error loading family data:', err);
  });
}

// Export default function
export default createFamilyTree;

// Auto-run if not imported (với data từ file)
if (import.meta.url === window.location.href) {
  createFamilyTree();
}
