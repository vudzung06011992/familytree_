import d3 from "../../d3.js"

// Simple sidebar functionality for family tree cards
export function createSidebar() {
  // Remove existing sidebar if any
  d3.select('#family-sidebar').remove();
  
  // Create simple sidebar element
  const sidebar = d3.select('body')
    .append('div')
    .attr('id', 'family-sidebar')
    .style('position', 'fixed')
    .style('top', '0')
    .style('right', '-400px') // Start hidden off-screen, wider sidebar
    .style('width', '400px') // Increased width
    .style('height', '100vh')
    .style('background-color', 'white')
    .style('color', 'black')
    .style('padding', '20px')
    .style('box-sizing', 'border-box')
    .style('font-family', 'Arial, sans-serif')
    .style('z-index', '10000')
    .style('transition', 'right 0.3s ease')
    .style('overflow-y', 'auto')
    .style('border-left', '1px solid #ccc')
    .style('box-shadow', '-2px 0 5px rgba(0,0,0,0.1)');
  
  // Add simple close button
  sidebar.append('button')
    .style('position', 'absolute')
    .style('top', '10px')
    .style('right', '10px')
    .style('background', 'none')
    .style('border', '1px solid #ccc')
    .style('font-size', '20px') // Larger close button
    .style('cursor', 'pointer')
    .style('padding', '8px 12px')
    .text('×')
    .on('click', () => hideSidebar(sidebar));
  
  // Add content container
  sidebar.append('div')
    .attr('id', 'sidebar-content')
    .style('margin-top', '40px');
  
  return sidebar;
}

export function showSidebar(sidebar, data) {
  const personData = data.data.data;
  const contentContainer = sidebar.select('#sidebar-content');
  
  // Clear previous content
  contentContainer.html('');
  
  // Simple title
  contentContainer.append('h3')
    .style('margin', '0 0 25px 0')
    .style('font-size', '22px') // Larger title
    .style('border-bottom', '1px solid #ccc')
    .style('padding-bottom', '10px')
    .text('Person Information');
  
  // Display information in simple format - same line
  const infoItems = [
    { label: 'Name', value: `${(personData['first name'] || '')} ${(personData['last name'] || '')}`.trim() },
    { label: 'Date of Birth', value: personData.birthday },
    { label: 'Gender', value: personData.gender === 'M' ? 'Male' : personData.gender === 'F' ? 'Female' : personData.gender },
    { label: 'Occupation', value: personData.occupation },
    { label: 'Location', value: personData.location },
    { label: 'Phone', value: personData.phone },
    { label: 'Email', value: personData.email }
  ];
  
  // Add all available information - single line format
  infoItems.forEach(item => {
    if (item.value) {
      contentContainer.append('div')
        .style('margin-bottom', '18px') // More spacing between items
        .style('font-size', '16px') // Larger font
        .style('line-height', '1.4')
        .html(`<strong>${item.label}:</strong> ${item.value}`);
    }
  });
  
  // Add any additional fields - single line format
  const displayedFields = ['first name', 'last name', 'birthday', 'gender', 'occupation', 'location', 'phone', 'email'];
  const additionalFields = Object.keys(personData).filter(key => 
    !displayedFields.includes(key) && 
    personData[key] && 
    personData[key].toString().trim() !== ''
  );
  
  additionalFields.forEach(field => {
    contentContainer.append('div')
      .style('margin-bottom', '18px') // More spacing
      .style('font-size', '16px') // Larger font
      .style('line-height', '1.4')
      .html(`<strong>${field.charAt(0).toUpperCase() + field.slice(1)}:</strong> ${personData[field]}`);
  });
  
  // Show message if no data
  if (contentContainer.selectAll('div').empty()) {
    contentContainer.append('div')
      .style('color', '#666')
      .style('font-style', 'italic')
      .style('font-size', '16px') // Larger font for no data message
      .text('No information available');
  }
  
  // Show the sidebar
  sidebar.style('right', '0px');
}

export function hideSidebar(sidebar) {
  sidebar.style('right', '-400px'); // Updated to match new width
}

// Legacy functions for compatibility
export function createTooltip() {
  return createSidebar();
}

export function showTooltip(sidebar, event, data) {
  showSidebar(sidebar, data);
}

export function updateTooltipPosition(sidebar, event) {
  // No positioning needed for sidebar
}

export function hideTooltip(sidebar) {
  hideSidebar(sidebar);
}
