import f3 from './index_support.js'

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
      }),
      // Initialize handlers for click events and sidebar
      cardHandlers = f3.handlers.cardMethods(store);

    // Enable interactive features
    store.setOnUpdate(props => {
      f3.view(store.getTree(), svg, Card, props || {});
      
      // Bind click events to cards after rendering
      svg.selectAll('.card').on('click', (event, d) => {
        // Focus on clicked person
        store.updateTree({tree_position: d.id});
        
        // Show person info in sidebar
        showPersonInfo(d);
      });
    });
    
    // Sidebar functionality
    function showPersonInfo(person) {
      const sidebar = document.getElementById('sidebar');
      const personInfo = document.getElementById('person-info');
      
      // Populate person info
      const data = person.data;
      const fullName = `${data["first name"] || ''} ${data["last name"] || ''}`.trim();
      
      personInfo.innerHTML = `
        <h4>${fullName}</h4>
        <p><strong>Năm sinh:</strong> ${data["birthday"] || 'Không rõ'}</p>
        <p><strong>Giới tính:</strong> ${data["gender"] || 'Không rõ'}</p>
        <p><strong>Quốc tịch:</strong> ${data["nationality"] || 'Không rõ'}</p>
        <p><strong>Nơi sinh:</strong> ${data["place of birth"] || 'Không rõ'}</p>
        <p><strong>Nghề nghiệp:</strong> ${data["occupation"] || 'Không rõ'}</p>
        <p><strong>Đặc điểm:</strong> ${data["characteristics"] || 'Không rõ'}</p>
        <p><strong>Điện thoại:</strong> ${data["phone"] || 'Không rõ'}</p>
        <p><strong>Email:</strong> ${data["email"] || 'Không rõ'}</p>
      `;
      
      // Show sidebar
      sidebar.style.right = '0px';
    }
    
    // Close sidebar functionality
    document.getElementById('sidebar-close').addEventListener('click', () => {
      document.getElementById('sidebar').style.right = '-300px';
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
