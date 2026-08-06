// Shared Faculty -> Department data for Nelavista's profile forms.
// Department names for LASU-curriculum departments (Biochemistry, Mathematics,
// Botany, Chemistry, Fisheries, Microbiology, Physics, Science Laboratory
// Technology, Biology, Computer Science, Accounting, Agriculture, Business
// Administration, Information Technology, Zoology, Entrepreneurship) match the
// exact strings used as keys in COURSE_CODES_DB["Lagos State University"] in
// materials.html -- changing these strings would silently break the "full
// curriculum available" match for those departments.
//
// Faculty names cover the real naming variation across Nigerian universities
// (e.g. "Management Sciences" vs "Business Administration" vs "Administration"
// are different names different schools use for essentially the same faculty)
// rather than a single NUC-standard list, since a student picks whatever name
// their own school actually uses.

const FACULTY_DEPARTMENTS = {
  "Science": {
    emoji: "🔬",
    departments: [
      { value: "Biochemistry", emoji: "🧬", hasCurriculum: true },
      { value: "Mathematics", emoji: "📐", hasCurriculum: true },
      { value: "Botany", emoji: "🌿", hasCurriculum: true },
      { value: "Chemistry", emoji: "⚗️", hasCurriculum: true },
      { value: "Fisheries", emoji: "🐟", hasCurriculum: true },
      { value: "Microbiology", emoji: "🔬", hasCurriculum: true },
      { value: "Physics", emoji: "⚛️", hasCurriculum: true },
      { value: "Science Laboratory Technology", emoji: "🧪", hasCurriculum: true },
      { value: "Biology", emoji: "🧫", hasCurriculum: true },
      { value: "Computer Science", emoji: "💻", hasCurriculum: true },
      { value: "Zoology", emoji: "🐾", hasCurriculum: true },
      { value: "Statistics", emoji: "📊" },
      { value: "Geology", emoji: "🪨" },
      { value: "Industrial Chemistry", emoji: "🏭" },
      { value: "Actuarial Science", emoji: "📈" },
      { value: "Marine Biology", emoji: "🐠" },
      { value: "Cell Biology and Genetics", emoji: "🧬" },
    ]
  },
  "Physical Sciences": {
    emoji: "🔭",
    departments: [
      { value: "Physics", emoji: "⚛️", hasCurriculum: true },
      { value: "Chemistry", emoji: "⚗️", hasCurriculum: true },
      { value: "Mathematics", emoji: "📐", hasCurriculum: true },
      { value: "Geology", emoji: "🪨" },
      { value: "Computer Science", emoji: "💻", hasCurriculum: true },
      { value: "Statistics", emoji: "📊" },
    ]
  },
  "Life Sciences": {
    emoji: "🧬",
    departments: [
      { value: "Botany", emoji: "🌿", hasCurriculum: true },
      { value: "Zoology", emoji: "🐾", hasCurriculum: true },
      { value: "Microbiology", emoji: "🔬", hasCurriculum: true },
      { value: "Biochemistry", emoji: "🧬", hasCurriculum: true },
      { value: "Biology", emoji: "🧫", hasCurriculum: true },
      { value: "Marine Sciences", emoji: "🌊" },
    ]
  },
  "Arts": {
    emoji: "🎨",
    departments: [
      { value: "English Language", emoji: "📖" },
      { value: "History", emoji: "🏛️" },
      { value: "Philosophy", emoji: "🤔" },
      { value: "Linguistics", emoji: "🗣️" },
      { value: "Yoruba", emoji: "🗣️" },
      { value: "Igbo", emoji: "🗣️" },
      { value: "Hausa", emoji: "🗣️" },
      { value: "French", emoji: "🇫🇷" },
      { value: "Theatre Arts", emoji: "🎭" },
      { value: "Music", emoji: "🎵" },
      { value: "Fine Arts", emoji: "🖌️" },
      { value: "Christian Religious Studies", emoji: "✝️" },
      { value: "Islamic Studies", emoji: "☪️" },
      { value: "Archaeology", emoji: "🏺" },
      { value: "Creative Arts", emoji: "🎨" },
    ]
  },
  "Humanities": {
    emoji: "📜",
    departments: [
      { value: "English Language", emoji: "📖" },
      { value: "History and International Studies", emoji: "🏛️" },
      { value: "Philosophy", emoji: "🤔" },
      { value: "Linguistics and African Languages", emoji: "🗣️" },
      { value: "Religious Studies", emoji: "🕊️" },
      { value: "Performing Arts", emoji: "🎭" },
    ]
  },
  "Social Sciences": {
    emoji: "🌍",
    departments: [
      { value: "Economics", emoji: "💰" },
      { value: "Political Science", emoji: "🏛️" },
      { value: "Sociology", emoji: "👥" },
      { value: "Psychology", emoji: "🧠" },
      { value: "Mass Communication", emoji: "📡" },
      { value: "Geography", emoji: "🗺️" },
      { value: "International Relations", emoji: "🌐" },
      { value: "Social Work", emoji: "🤝" },
      { value: "Public Administration", emoji: "🏢" },
      { value: "Demography and Social Statistics", emoji: "📊" },
    ]
  },
  "Law": {
    emoji: "⚖️",
    departments: [
      { value: "Common Law", emoji: "⚖️" },
      { value: "Private and Property Law", emoji: "📜" },
      { value: "Public Law", emoji: "🏛️" },
      { value: "Islamic Law", emoji: "☪️" },
      { value: "Commercial and Industrial Law", emoji: "💼" },
      { value: "International Law", emoji: "🌐" },
      { value: "Jurisprudence and International Law", emoji: "⚖️" },
    ]
  },
  "Engineering": {
    emoji: "⚙️",
    departments: [
      { value: "Civil Engineering", emoji: "🏗️" },
      { value: "Mechanical Engineering", emoji: "⚙️" },
      { value: "Electrical/Electronics Engineering", emoji: "🔌" },
      { value: "Chemical Engineering", emoji: "🧪" },
      { value: "Petroleum Engineering", emoji: "🛢️" },
      { value: "Computer Engineering", emoji: "💻" },
      { value: "Agricultural Engineering", emoji: "🚜" },
      { value: "Systems Engineering", emoji: "🔧" },
      { value: "Metallurgical and Materials Engineering", emoji: "⚙️" },
      { value: "Water Resources Engineering", emoji: "💧" },
      { value: "Biomedical Engineering", emoji: "🩺" },
      { value: "Mechatronics Engineering", emoji: "🤖" },
      { value: "Marine Engineering", emoji: "⚓" },
      { value: "Structural Engineering", emoji: "🏗️" },
      { value: "Food Engineering", emoji: "🍞" },
    ]
  },
  "Education": {
    emoji: "📚",
    departments: [
      { value: "Educational Administration and Planning", emoji: "🏫" },
      { value: "Educational Psychology", emoji: "🧠" },
      { value: "Guidance and Counselling", emoji: "🧭" },
      { value: "Curriculum Studies", emoji: "📋" },
      { value: "Adult Education", emoji: "👨‍🏫" },
      { value: "Science Education", emoji: "🔬" },
      { value: "Physical and Health Education", emoji: "🏃" },
      { value: "Special Education", emoji: "💙" },
      { value: "Library and Information Science", emoji: "📚" },
      { value: "Early Childhood Education", emoji: "🧸" },
      { value: "Social Studies Education", emoji: "🌍" },
      { value: "Business Education", emoji: "💼" },
      { value: "Educational Technology", emoji: "💻" },
    ]
  },
  "Vocational and Technical Education": {
    emoji: "🛠️",
    departments: [
      { value: "Agricultural Education", emoji: "🌾" },
      { value: "Business Education", emoji: "💼" },
      { value: "Home Economics Education", emoji: "🏠" },
      { value: "Industrial Technology Education", emoji: "🏭" },
      { value: "Technical Education", emoji: "🔧" },
    ]
  },
  "Management Sciences": {
    emoji: "💼",
    departments: [
      { value: "Accounting", emoji: "📋", hasCurriculum: true },
      { value: "Business Administration", emoji: "🏢", hasCurriculum: true },
      { value: "Banking and Finance", emoji: "🏦" },
      { value: "Marketing", emoji: "📣" },
      { value: "Insurance", emoji: "🛡️" },
      { value: "Actuarial Science", emoji: "📈" },
      { value: "Human Resource Management", emoji: "👥" },
      { value: "Industrial Relations and Personnel Management", emoji: "🤝" },
      { value: "Entrepreneurship", emoji: "💡", hasCurriculum: true },
      { value: "Taxation", emoji: "🧾" },
      { value: "Office and Information Management", emoji: "🗂️" },
    ]
  },
  "Business Administration": {
    emoji: "🏢",
    departments: [
      { value: "Business Administration", emoji: "🏢", hasCurriculum: true },
      { value: "Accounting", emoji: "📋", hasCurriculum: true },
      { value: "Marketing", emoji: "📣" },
      { value: "Banking and Finance", emoji: "🏦" },
      { value: "Entrepreneurship", emoji: "💡", hasCurriculum: true },
      { value: "Human Resource Management", emoji: "👥" },
    ]
  },
  "Administration": {
    emoji: "🏛️",
    departments: [
      { value: "Public Administration", emoji: "🏢" },
      { value: "Local Government Studies", emoji: "🏘️" },
      { value: "Accounting", emoji: "📋", hasCurriculum: true },
      { value: "Business Administration", emoji: "🏢", hasCurriculum: true },
    ]
  },
  "Medicine": {
    emoji: "🏥",
    departments: [
      { value: "Medicine and Surgery (MBBS)", emoji: "🩺" },
      { value: "Anatomy", emoji: "🦴" },
      { value: "Physiology", emoji: "🫀" },
      { value: "Medical Biochemistry", emoji: "🧬" },
      { value: "Pathology", emoji: "🔬" },
      { value: "Community Health", emoji: "🏘️" },
      { value: "Pharmacology", emoji: "💊" },
      { value: "Public Health", emoji: "🌍" },
      { value: "Radiography", emoji: "📷" },
      { value: "Medical Laboratory Science", emoji: "🧪" },
    ]
  },
  "Basic Medical Sciences": {
    emoji: "🩺",
    departments: [
      { value: "Anatomy", emoji: "🦴" },
      { value: "Physiology", emoji: "🫀" },
      { value: "Medical Biochemistry", emoji: "🧬" },
      { value: "Nursing Science", emoji: "👩‍⚕️" },
      { value: "Physiotherapy", emoji: "🏃" },
      { value: "Medical Laboratory Science", emoji: "🧪" },
      { value: "Radiography", emoji: "📷" },
      { value: "Public Health", emoji: "🌍" },
    ]
  },
  "Clinical Sciences": {
    emoji: "🩺",
    departments: [
      { value: "Medicine and Surgery (MBBS)", emoji: "🩺" },
      { value: "Obstetrics and Gynaecology", emoji: "🤰" },
      { value: "Paediatrics", emoji: "👶" },
      { value: "Surgery", emoji: "🔪" },
      { value: "Internal Medicine", emoji: "🩻" },
      { value: "Psychiatry", emoji: "🧠" },
    ]
  },
  "Dentistry": {
    emoji: "🦷",
    departments: [
      { value: "Dental Surgery", emoji: "🦷" },
      { value: "Oral Pathology", emoji: "🔬" },
      { value: "Preventive Dentistry", emoji: "🪥" },
      { value: "Oral and Maxillofacial Surgery", emoji: "🦴" },
    ]
  },
  "Pharmacy": {
    emoji: "💊",
    departments: [
      { value: "Pharmacy", emoji: "💊" },
      { value: "Pharmacology", emoji: "🧪" },
      { value: "Pharmaceutical Chemistry", emoji: "⚗️" },
      { value: "Pharmacognosy", emoji: "🌿" },
      { value: "Clinical Pharmacy", emoji: "🏥" },
      { value: "Pharmaceutics", emoji: "💊" },
    ]
  },
  "Veterinary Medicine": {
    emoji: "🐕",
    departments: [
      { value: "Veterinary Medicine", emoji: "🐕" },
      { value: "Veterinary Anatomy", emoji: "🦴" },
      { value: "Veterinary Physiology", emoji: "🫀" },
      { value: "Veterinary Pathology", emoji: "🔬" },
      { value: "Animal Health and Production", emoji: "🐄" },
    ]
  },
  "Agriculture": {
    emoji: "🌾",
    departments: [
      { value: "Agriculture", emoji: "🌾", hasCurriculum: true },
      { value: "Agricultural Economics", emoji: "💰" },
      { value: "Animal Science", emoji: "🐄" },
      { value: "Crop Science", emoji: "🌱" },
      { value: "Soil Science", emoji: "🟤" },
      { value: "Agricultural Extension and Rural Development", emoji: "🚜" },
      { value: "Food Science and Technology", emoji: "🍞" },
      { value: "Forestry and Wood Technology", emoji: "🌲" },
      { value: "Fisheries", emoji: "🐟", hasCurriculum: true },
      { value: "Agronomy", emoji: "🌾" },
      { value: "Home Science and Management", emoji: "🏠" },
    ]
  },
  "Renewable Natural Resources": {
    emoji: "🌲",
    departments: [
      { value: "Forestry", emoji: "🌲" },
      { value: "Wildlife and Ecotourism Management", emoji: "🦁" },
      { value: "Fisheries", emoji: "🐟", hasCurriculum: true },
      { value: "Wood Products Engineering", emoji: "🪵" },
    ]
  },
  "Environmental Sciences": {
    emoji: "🏙️",
    departments: [
      { value: "Architecture", emoji: "🏛️" },
      { value: "Urban and Regional Planning", emoji: "🗺️" },
      { value: "Estate Management", emoji: "🏘️" },
      { value: "Building Technology", emoji: "🏗️" },
      { value: "Surveying and Geoinformatics", emoji: "📐" },
      { value: "Quantity Surveying", emoji: "📏" },
      { value: "Environmental Management", emoji: "🌳" },
    ]
  },
  "Environmental Design": {
    emoji: "🏛️",
    departments: [
      { value: "Architecture", emoji: "🏛️" },
      { value: "Urban and Regional Planning", emoji: "🗺️" },
      { value: "Building Technology", emoji: "🏗️" },
      { value: "Quantity Surveying", emoji: "📏" },
    ]
  },
  "Nursing": {
    emoji: "👩‍⚕️",
    departments: [
      { value: "Nursing Science", emoji: "👩‍⚕️" },
      { value: "Public Health Nursing", emoji: "🌍" },
      { value: "Midwifery", emoji: "🤰" },
      { value: "Mental Health Nursing", emoji: "🧠" },
    ]
  },
  "Allied Health Sciences": {
    emoji: "🩺",
    departments: [
      { value: "Physiotherapy", emoji: "🏃" },
      { value: "Medical Laboratory Science", emoji: "🧪" },
      { value: "Radiography", emoji: "📷" },
      { value: "Optometry", emoji: "👓" },
      { value: "Prosthetics and Orthotics", emoji: "🦾" },
      { value: "Environmental Health Science", emoji: "🌍" },
    ]
  },
  "Computing": {
    emoji: "💻",
    departments: [
      { value: "Computer Science", emoji: "💻", hasCurriculum: true },
      { value: "Information Technology", emoji: "🖥️", hasCurriculum: true },
      { value: "Cyber Security", emoji: "🔐" },
      { value: "Software Engineering", emoji: "👨‍💻" },
      { value: "Information Systems", emoji: "🗄️" },
      { value: "Data Science", emoji: "📊" },
    ]
  },
  "Communication and Information Sciences": {
    emoji: "📡",
    departments: [
      { value: "Mass Communication", emoji: "📡" },
      { value: "Library and Information Science", emoji: "📚" },
      { value: "Telecommunication Science", emoji: "📶" },
      { value: "Information Technology", emoji: "🖥️", hasCurriculum: true },
    ]
  },
  "Communication and Media Studies": {
    emoji: "🎥",
    departments: [
      { value: "Journalism", emoji: "📰" },
      { value: "Broadcasting", emoji: "📻" },
      { value: "Public Relations and Advertising", emoji: "📣" },
      { value: "Film and Multimedia Studies", emoji: "🎥" },
    ]
  },
  "Earth Sciences": {
    emoji: "🌋",
    departments: [
      { value: "Geology", emoji: "🪨" },
      { value: "Geophysics", emoji: "🌍" },
      { value: "Meteorology", emoji: "⛅" },
      { value: "Petroleum Geoscience", emoji: "🛢️" },
    ]
  },
  "Transport": {
    emoji: "🚢",
    departments: [
      { value: "Maritime Transport Management", emoji: "🚢" },
      { value: "Logistics and Transport Technology", emoji: "🚚" },
      { value: "Transport Planning", emoji: "🗺️" },
    ]
  },
  "Islamic Studies": {
    emoji: "☪️",
    departments: [
      { value: "Islamic Studies", emoji: "☪️" },
      { value: "Arabic Language", emoji: "🗣️" },
      { value: "Shariah", emoji: "📜" },
    ]
  },
  "Theology": {
    emoji: "✝️",
    departments: [
      { value: "Theology", emoji: "✝️" },
      { value: "Christian Religious Studies", emoji: "📖" },
      { value: "Biblical Studies", emoji: "📖" },
      { value: "Church History", emoji: "⛪" },
    ]
  },
};

// "General Studies" (GST/GNS) applies to every student regardless of faculty
// or department -- handled separately as COURSE_CODES_DB's "_general" key,
// not listed as its own faculty here.
