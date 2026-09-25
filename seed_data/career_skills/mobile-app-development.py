"""Seed data for the Mobile App Development 30-Day Skill Class."""

SKILL = {
    "slug": "mobile-app-development",
    "name": "Mobile App Development",
    "tagline": "Build real Android and iOS apps with React Native and ship one to a phone, not just a simulator.",
    "description": "Mobile app development is the skill of building the apps that run on the phones nearly every Nigerian carries, from banking apps to delivery platforms to campus tools. It is one of the highest-demand tech skills in the local job market because fintech, logistics, and edtech startups are mobile-first by default, and a single working app on your phone is stronger proof of skill than any certificate. This track takes you from zero to building a real cross-platform app with React Native, complete with navigation, data persistence, and a live API connection, ready to demo to an employer or client.",
    "level": "beginner",
    "estimated_hours": 62,
    "course_title": "30-Day Mobile App Development Career Track",
    "course_description": "After 30 days you will be able to design, build, and debug multi-screen cross-platform mobile apps with React Native, persist data locally, connect to real APIs, and package an app for demo and portfolio use.",
    "final_project": {
        "title": "Build and Demo a Multi-Screen Mobile App",
        "description": "Design, build, and demo a real mobile app such as a campus events tracker, a personal budget app, a study group finder, or a local services directory. The app must have at least four distinct screens connected with real navigation, must persist user data locally so it survives an app restart, and must fetch live data from at least one real API. It must include proper loading and error states, a clean and consistent UI, and be run on a physical device or emulator for a recorded demo. This is the kind of working, demoable app that convinces a hiring manager or client you can ship real mobile software, not just follow a tutorial.",
        "difficulty": "advanced",
        "estimated_hours": 12,
        "skills_demonstrated": ["React Native", "mobile navigation", "local data persistence", "REST API integration", "state management", "UI/UX for mobile", "debugging on device"],
        "rubric": [
            {"name": "Multi-screen navigation and app structure", "max_points": 25},
            {"name": "Data persistence and API integration", "max_points": 30},
            {"name": "UI quality and mobile UX", "max_points": 25},
            {"name": "Working demo and code documentation", "max_points": 20}
        ]
    },
    "days": [
        {
            "day_number": 1,
            "week_number": 1,
            "week_title": "How Mobile Apps Actually Work",
            "title": "Native, Cross-Platform, and Web Apps: Picking Your Path",
            "learning_objective": "By the end of this class, you will be able to explain the difference between native, cross-platform, and web apps and why this track uses React Native.",
            "duration_minutes": 20,
            "content_html": """<p>Every app on your phone was built one of a few ways, and knowing the difference matters before you write a single line of code, because it shapes what jobs you can apply for and what tools you will learn. Getting this wrong wastes months learning the wrong stack.</p><h2>Native vs Cross-Platform vs Web</h2><p><strong>Native apps</strong> are built specifically for one platform: Swift/Kotlin for iOS, Kotlin/Java for Android. They perform best but require maintaining two separate codebases. <strong>Cross-platform apps</strong> use one codebase, written in a framework like React Native or Flutter, to produce apps for both iOS and Android. <strong>Web apps</strong> just run in a mobile browser and are not installed at all.</p><pre><code>Native:         iOS app (Swift) + Android app (Kotlin) = 2 codebases
Cross-platform: React Native app = 1 codebase -> iOS + Android
Web app:        Runs in browser, no install, limited device access</code></pre><h2>Why This Track Uses React Native</h2><p>React Native lets you write one JavaScript codebase that compiles to real native apps on both platforms, which is why companies like Flutterwave-adjacent startups and many Nigerian fintechs use it or Flutter to move fast with a small team. It also means the JavaScript skills you build here transfer directly to web development, doubling your employability. By day 30 you will have a real app running on an actual phone, not just a browser tab.</p>""",
            "key_concepts": ["native apps", "cross-platform apps", "React Native", "single codebase", "iOS vs Android"],
            "practical_exercise": {
                "title": "Audit Three Apps on Your Phone",
                "instructions": "Pick three apps installed on your own phone (or a friend's) and research whether each is built natively, cross-platform, or as a web wrapper, using each company's engineering blog or job postings as evidence. Write two to three sentences per app explaining what you found and why you think the company chose that approach. Submit your three short write-ups."
            },
            "quiz": [
                {"question": "What is the main advantage of a cross-platform framework like React Native?", "options": ["It only works on Android", "One codebase can produce apps for both iOS and Android", "It cannot access device hardware", "It is only used for web pages"], "correct_index": 1, "explanation": "React Native compiles one JavaScript codebase into real native apps for both iOS and Android, saving development time."},
                {"question": "Which languages are typically used for native Android development?", "options": ["Swift and Objective-C", "HTML and CSS", "Kotlin and Java", "React Native and Flutter"], "correct_index": 2, "explanation": "Native Android apps are traditionally built with Java or Kotlin, while native iOS apps use Swift or Objective-C."},
                {"question": "Why do many startups choose React Native or Flutter over building two native apps?", "options": ["Native apps are illegal to build", "Cross-platform apps cannot use the camera or GPS", "There is no difference in cost or speed", "It lets a small team ship to both platforms faster with one codebase"], "correct_index": 3, "explanation": "Cross-platform frameworks let smaller teams move faster by maintaining a single codebase instead of two separate native ones."}
            ],
            "resources": [
                {"label": "React Native Documentation", "url": "https://reactnative.dev/docs/getting-started"}
            ]
        },
        {
            "day_number": 2,
            "week_number": 1,
            "week_title": "How Mobile Apps Actually Work",
            "title": "Setting Up Your React Native Development Environment with Expo",
            "learning_objective": "By the end of this class, you will be able to set up a working React Native project using Expo and run it on your own phone.",
            "duration_minutes": 30,
            "content_html": """<p>Before you can build anything, you need a development environment that lets you see your code running on an actual device, ideally without needing an expensive Mac or complex native build tools. Expo solves this and is what most React Native beginners and many production teams use today.</p><h2>Installing Node.js and Creating an Expo App</h2><p>Expo is a toolchain built on top of React Native that handles the native build complexity for you, letting you run your app instantly via a QR code using the Expo Go app on your own phone.</p><pre><code>npx create-expo-app MyFirstApp
cd MyFirstApp
npx expo start</code></pre><h2>Running on a Real Device</h2><p>After running <code>npx expo start</code>, a QR code appears in your terminal. Install the Expo Go app from the Play Store or App Store on your phone, scan the code, and your app loads live on your device. Any code change you save appears on your phone within seconds, a feature called hot reload that dramatically speeds up development compared to native workflows requiring a full rebuild.</p><p>This exact setup, Expo plus a physical device, is what you will use for the rest of this track, including your final project demo.</p>""",
            "key_concepts": ["Node.js", "Expo CLI", "Expo Go app", "hot reload", "npx create-expo-app"],
            "practical_exercise": {
                "title": "Run Your First App on Your Phone",
                "instructions": "Install Node.js, create a new Expo app with npx create-expo-app, install Expo Go on your phone, and scan the QR code to run it live. Change the default text in App.js to your name and confirm it updates on your phone via hot reload. Submit a screenshot of your app running on your device."
            },
            "quiz": [
                {"question": "What does the Expo Go app allow you to do?", "options": ["Compile apps for the App Store directly", "Run your in-progress React Native app live on a physical phone", "Design UI mockups", "Host a backend server"], "correct_index": 1, "explanation": "Expo Go lets developers scan a QR code and run their app instantly on a real device without a full native build."},
                {"question": "What command creates a new Expo project?", "options": ["npm start expo", "expo new-project", "npx create-expo-app", "react-native init"], "correct_index": 2, "explanation": "npx create-expo-app scaffolds a new Expo-based React Native project."},
                {"question": "What is 'hot reload'?", "options": ["A way to restart your phone", "A method for compressing images", "A type of app crash", "Code changes appearing live on the running app within seconds of saving"], "correct_index": 3, "explanation": "Hot reload automatically updates the running app almost instantly after a code change is saved, speeding up development."}
            ],
            "resources": [
                {"label": "Expo Documentation", "url": "https://docs.expo.dev/"}
            ]
        },
        {
            "day_number": 3,
            "week_number": 1,
            "week_title": "How Mobile Apps Actually Work",
            "title": "Building Your First Screen with Core React Native Components",
            "learning_objective": "By the end of this class, you will be able to build a simple screen using View, Text, Image, and StyleSheet.",
            "duration_minutes": 25,
            "content_html": """<p>Unlike web development, React Native does not use HTML tags like div or p. Instead it has its own set of core components that map to real native UI elements on iOS and Android, and learning these is the first real building block of any app you will build this month.</p><h2>The Core Components</h2><p><strong>View</strong> is the equivalent of a div, a container for layout. <strong>Text</strong> displays text (unlike the web, raw text cannot float outside a Text component). <strong>Image</strong> renders images from a local file or a URL.</p><pre><code>import { View, Text, Image, StyleSheet } from "react-native";

export default function ProfileScreen() {
  return (
    &lt;View style={styles.container}&gt;
      &lt;Image source={{ uri: "https://placekitten.com/100/100" }} style={styles.avatar} /&gt;
      &lt;Text style={styles.name}&gt;Ada Okafor&lt;/Text&gt;
    &lt;/View&gt;
  );
}

const styles = StyleSheet.create({
  container: { alignItems: "center", padding: 20 },
  avatar: { width: 100, height: 100, borderRadius: 50 },
  name: { fontSize: 20, fontWeight: "bold", marginTop: 10 },
});</code></pre><h2>Styling with StyleSheet</h2><p>React Native styling uses JavaScript objects, written with camelCase properties like <code>backgroundColor</code> instead of CSS's <code>background-color</code>. <code>StyleSheet.create</code> is the standard way to organize these styles, and most of the layout rules you may know from CSS Flexbox apply directly, since View defaults to Flexbox layout.</p>""",
            "key_concepts": ["View component", "Text component", "Image component", "StyleSheet.create", "Flexbox default layout"],
            "practical_exercise": {
                "title": "Build a Profile Screen",
                "instructions": "Build a single profile screen using View, Image, and Text components showing a profile picture, a name, and a one-line bio, styled with StyleSheet.create. Run it on your phone using Expo Go. Submit your component code and a screenshot from your device."
            },
            "quiz": [
                {"question": "Which component must wrap any raw text in React Native?", "options": ["View", "Text", "Image", "StyleSheet"], "correct_index": 1, "explanation": "Unlike the web, React Native requires all text to be inside a Text component; it cannot float freely inside a View."},
                {"question": "What layout system does View use by default?", "options": ["CSS Grid", "Table layout", "Flexbox", "Absolute positioning only"], "correct_index": 2, "explanation": "React Native's View component defaults to Flexbox layout, similar to setting display: flex in CSS."},
                {"question": "How are styles typically defined in React Native?", "options": ["In separate .css files only", "Using StyleSheet.create with camelCase JavaScript properties", "Inline HTML style attributes", "React Native does not support styling"], "correct_index": 1, "explanation": "React Native styles are JavaScript objects, commonly organized with StyleSheet.create, using camelCase property names."}
            ],
            "resources": [
                {"label": "React Native Core Components", "url": "https://reactnative.dev/docs/components-and-apis"}
            ]
        },
        {
            "day_number": 4,
            "week_number": 1,
            "week_title": "How Mobile Apps Actually Work",
            "title": "Making Screens Interactive with State and Touch Events",
            "learning_objective": "By the end of this class, you will be able to build an interactive screen using useState and touch event handlers.",
            "duration_minutes": 30,
            "content_html": """<p>A screen that only displays static text is not an app, it is a poster. What makes something an app is interactivity: buttons that respond to taps, counters that update, forms that react as you type. React Native handles this with the same useState hook used in React for the web.</p><h2>useState and TouchableOpacity</h2><p>useState lets a component remember and update a value across re-renders. TouchableOpacity is the standard way to make anything tappable, with a visual dimming effect on press to give the user feedback.</p><pre><code>import { useState } from "react";
import { View, Text, TouchableOpacity, StyleSheet } from "react-native";

export default function CounterScreen() {
  const [count, setCount] = useState(0);

  return (
    &lt;View style={styles.container}&gt;
      &lt;Text style={styles.count}&gt;{count}&lt;/Text&gt;
      &lt;TouchableOpacity style={styles.button} onPress={() =&gt; setCount(count + 1)}&gt;
        &lt;Text style={styles.buttonText}&gt;Add One&lt;/Text&gt;
      &lt;/TouchableOpacity&gt;
    &lt;/View&gt;
  );
}

const styles = StyleSheet.create({
  container: { alignItems: "center", marginTop: 60 },
  count: { fontSize: 40, marginBottom: 20 },
  button: { backgroundColor: "#2563eb", padding: 14, borderRadius: 8 },
  buttonText: { color: "white", fontWeight: "bold" },
});</code></pre><h2>Why This Matters</h2><p>Every real feature you will build this month, from a login form to a like button, is built on this exact pattern: state that changes, and a touch handler that changes it. Mastering this now makes every later day faster.</p>""",
            "key_concepts": ["useState hook", "TouchableOpacity", "onPress handler", "re-rendering", "component state"],
            "practical_exercise": {
                "title": "Build a Tap Counter App",
                "instructions": "Build a screen with a number displayed on screen, an 'Add One' button, and a 'Reset' button, both using useState and TouchableOpacity. Style the buttons with clear visual feedback. Submit your code and a short screen recording or GIF of it working on your phone."
            },
            "quiz": [
                {"question": "What does the useState hook do?", "options": ["Deletes a component", "Lets a component store and update a value that persists across re-renders", "Connects to a database", "Handles network requests"], "correct_index": 1, "explanation": "useState creates a piece of state a component can read and update, triggering a re-render when it changes."},
                {"question": "Which component is commonly used to make something tappable in React Native?", "options": ["Text", "StyleSheet", "Image", "TouchableOpacity"], "correct_index": 3, "explanation": "TouchableOpacity wraps content to make it respond to taps, with a dimming effect for visual feedback."},
                {"question": "What triggers a React Native component to re-render?", "options": ["Restarting the phone", "Closing the Expo Go app", "Its state or props changing", "Nothing, components never update"], "correct_index": 2, "explanation": "A component re-renders whenever its state (via useState) or props change, reflecting the new values on screen."}
            ],
            "resources": [
                {"label": "React Native: Handling Touches", "url": "https://reactnative.dev/docs/handling-touches"}
            ]
        },
        {
            "day_number": 5,
            "week_number": 1,
            "week_title": "How Mobile Apps Actually Work",
            "title": "Building Scrollable Lists with FlatList",
            "learning_objective": "By the end of this class, you will be able to render a scrollable, performant list of data using FlatList.",
            "duration_minutes": 25,
            "content_html": """<p>Almost every real app, from a food delivery app's restaurant list to a social feed, is built around one core UI pattern: a scrollable list of items. React Native provides FlatList specifically for this, and it is far more efficient than mapping over an array inside a plain View.</p><h2>Why FlatList Instead of .map()</h2><p>FlatList only renders the items currently visible on screen (plus a small buffer), recycling views as the user scrolls. This is called virtualization, and it is why a list of 5,000 items in FlatList stays smooth while the same list built with a plain scrollable View would lag badly.</p><pre><code>import { FlatList, View, Text, StyleSheet } from "react-native";

const products = [
  { id: "1", name: "Used Textbook" },
  { id: "2", name: "Desk Lamp" },
  { id: "3", name: "Bluetooth Speaker" },
];

export default function ListingsScreen() {
  return (
    &lt;FlatList
      data={products}
      keyExtractor={(item) =&gt; item.id}
      renderItem={({ item }) =&gt; (
        &lt;View style={styles.card}&gt;
          &lt;Text&gt;{item.name}&lt;/Text&gt;
        &lt;/View&gt;
      )}
    /&gt;
  );
}

const styles = StyleSheet.create({
  card: { padding: 16, borderBottomWidth: 1, borderColor: "#eee" },
});</code></pre><p>The <code>keyExtractor</code> prop is required and must return a unique string per item; using array index instead of a real id is a common bug that causes broken UI on reorder or deletion.</p>""",
            "key_concepts": ["FlatList", "list virtualization", "keyExtractor", "renderItem", "performance"],
            "practical_exercise": {
                "title": "Build a Scrollable Listings Screen",
                "instructions": "Create an array of at least 15 fake product or event objects, each with a unique id, name, and price, and render them in a FlatList with a styled card for each item. Confirm the list scrolls smoothly on your phone. Submit your code and a screenshot."
            },
            "quiz": [
                {"question": "Why is FlatList preferred over mapping a plain array inside a View for long lists?", "options": ["FlatList only works with text", "FlatList virtualizes rendering, only drawing visible items for better performance", "There is no difference in performance", "FlatList cannot scroll"], "correct_index": 1, "explanation": "FlatList renders only the items currently visible plus a buffer, keeping performance smooth even with thousands of items."},
                {"question": "What is the purpose of the keyExtractor prop?", "options": ["It sets the background color", "It sorts the list alphabetically", "It returns a unique string identifier for each list item", "It disables scrolling"], "correct_index": 2, "explanation": "keyExtractor gives FlatList a stable unique key per item, which is essential for correct rendering and updates."},
                {"question": "What is a common bug when keyExtractor uses the array index instead of a real unique id?", "options": ["UI can behave incorrectly when items are reordered, added, or removed", "The app will not compile", "The list will not scroll at all", "Images fail to load"], "correct_index": 0, "explanation": "Using index as a key breaks React's ability to correctly track items when the underlying list order or contents change."}
            ],
            "resources": [
                {"label": "React Native FlatList", "url": "https://reactnative.dev/docs/flatlist"}
            ]
        },
        {
            "day_number": 6,
            "week_number": 2,
            "week_title": "Navigation and Multi-Screen Apps",
            "title": "Setting Up Stack Navigation Between Screens",
            "learning_objective": "By the end of this class, you will be able to set up navigation between two or more screens using React Navigation.",
            "duration_minutes": 30,
            "content_html": """<p>No real app has just one screen. A shopping app has a home screen, a product detail screen, and a cart screen; a social app has a feed and profile pages. React Navigation is the standard library nearly every production React Native app uses to move between screens.</p><h2>Installing and Setting Up a Stack Navigator</h2><p>A stack navigator works like a stack of cards: navigating to a new screen pushes it on top, and going back pops it off, complete with the native back gesture and header your users already expect.</p><pre><code>npx expo install @react-navigation/native @react-navigation/native-stack

import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import HomeScreen from "./screens/HomeScreen";
import DetailScreen from "./screens/DetailScreen";

const Stack = createNativeStackNavigator();

export default function App() {
  return (
    &lt;NavigationContainer&gt;
      &lt;Stack.Navigator&gt;
        &lt;Stack.Screen name="Home" component={HomeScreen} /&gt;
        &lt;Stack.Screen name="Detail" component={DetailScreen} /&gt;
      &lt;/Stack.Navigator&gt;
    &lt;/NavigationContainer&gt;
  );
}</code></pre><h2>Navigating and Passing Data</h2><p>Every screen inside a Stack.Navigator receives a <code>navigation</code> prop automatically. Calling <code>navigation.navigate("Detail", { id: "1" })</code> moves to the Detail screen and passes data along with it, which you will use constantly once you connect real data to your app.</p>""",
            "key_concepts": ["React Navigation", "stack navigator", "navigation prop", "navigate() with params", "screen push/pop"],
            "practical_exercise": {
                "title": "Connect Two Screens with Navigation",
                "instructions": "Install React Navigation and build a Home screen with a button that navigates to a Detail screen, passing a piece of data (such as an id or name) as a param. Display the received param on the Detail screen. Submit your code and a screen recording showing the navigation working."
            },
            "quiz": [
                {"question": "What does a stack navigator do when you navigate to a new screen?", "options": ["It pushes the new screen on top, like adding a card to a stack", "It replaces the entire app", "It closes the app", "It deletes the previous screen from memory permanently"], "correct_index": 0, "explanation": "A stack navigator pushes new screens on top of previous ones, allowing the native back button/gesture to pop back."},
                {"question": "How do you pass data to another screen with React Navigation?", "options": ["Global variables only", "As a second argument to navigation.navigate()", "It is not possible to pass data between screens", "Only through a backend API"], "correct_index": 1, "explanation": "navigation.navigate('ScreenName', { param: value }) passes data as route params to the destination screen."},
                {"question": "What prop does every screen inside a Stack.Navigator automatically receive?", "options": ["style", "theme", "navigation", "database"], "correct_index": 2, "explanation": "React Navigation automatically injects a navigation prop into every screen component registered in the navigator."}
            ],
            "resources": [
                {"label": "React Navigation Documentation", "url": "https://reactnavigation.org/docs/getting-started"}
            ]
        },
        {
            "day_number": 7,
            "week_number": 2,
            "week_title": "Navigation and Multi-Screen Apps",
            "title": "Building Tab-Based Navigation for Multi-Section Apps",
            "learning_objective": "By the end of this class, you will be able to build a bottom tab navigator with multiple independent sections.",
            "duration_minutes": 25,
            "content_html": """<p>Open any major app, Instagram, a banking app, a delivery app, and you will see the same pattern at the bottom of the screen: a row of tabs like Home, Search, and Profile. This is bottom tab navigation, and it is the most common navigation pattern in mobile apps because users already know how to use it.</p><h2>Setting Up Bottom Tabs</h2><p>Tab navigators are usually combined with stack navigators: each tab can have its own internal stack of screens, so tapping into a post from the Home tab does not affect the Search tab's navigation state.</p><pre><code>npx expo install @react-navigation/bottom-tabs

import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
import HomeScreen from "./screens/HomeScreen";
import ProfileScreen from "./screens/ProfileScreen";

const Tab = createBottomTabNavigator();

function AppTabs() {
  return (
    &lt;Tab.Navigator&gt;
      &lt;Tab.Screen name="Home" component={HomeScreen} /&gt;
      &lt;Tab.Screen name="Profile" component={ProfileScreen} /&gt;
    &lt;/Tab.Navigator&gt;
  );
}</code></pre><h2>Why This Matters for Your Portfolio App</h2><p>Combining a bottom tab navigator with a stack navigator per tab is exactly the structure real production apps use, and it is what you will use for your own multi-screen app later in this track. Getting comfortable nesting navigators now avoids major restructuring later.</p>""",
            "key_concepts": ["bottom tab navigator", "nested navigators", "tab bar icons", "navigation architecture"],
            "practical_exercise": {
                "title": "Build a Three-Tab App",
                "instructions": "Install the bottom tabs package and build an app with three tabs (for example Home, Search, and Profile), each showing a distinct placeholder screen with a title. Confirm tapping each tab switches screens correctly on your device. Submit your code and a screen recording of tab switching."
            },
            "quiz": [
                {"question": "What is the most common location for tab navigation in mobile apps?", "options": ["The bottom of the screen", "The top of the screen only", "Inside a hidden side menu only", "There is no standard location"], "correct_index": 0, "explanation": "Bottom tab navigation, seen in apps like Instagram and most banking apps, is the dominant mobile navigation pattern."},
                {"question": "Why are tab navigators often combined with stack navigators per tab?", "options": ["It is required by Expo and cannot be avoided", "To make the app slower", "So each tab can maintain its own independent navigation history", "Tabs cannot contain more than one screen otherwise"], "correct_index": 2, "explanation": "Nesting a stack inside each tab lets users drill into detail screens within a tab without disrupting other tabs' navigation state."},
                {"question": "Which package provides bottom tab navigation in React Navigation?", "options": ["@react-navigation/native-stack", "@react-navigation/drawer", "@react-navigation/core", "@react-navigation/bottom-tabs"], "correct_index": 3, "explanation": "@react-navigation/bottom-tabs is the dedicated package for building bottom tab bar navigation."}
            ],
            "resources": [
                {"label": "React Navigation: Tab Navigation", "url": "https://reactnavigation.org/docs/tab-based-navigation"}
            ]
        },
        {
            "day_number": 8,
            "week_number": 2,
            "week_title": "Navigation and Multi-Screen Apps",
            "title": "Collecting User Input with Forms and TextInput",
            "learning_objective": "By the end of this class, you will be able to build a form screen with validated TextInput fields.",
            "duration_minutes": 30,
            "content_html": """<p>Login screens, signup forms, search bars, and settings screens all rely on the same core component: TextInput. Nearly every app you will ever build needs to collect input from a user correctly and give feedback when that input is invalid.</p><h2>Controlled TextInput</h2><p>Like web forms in React, TextInput is typically "controlled," meaning its value comes from state and updates through an onChangeText handler, rather than the input managing its own internal value.</p><pre><code>import { useState } from "react";
import { View, TextInput, Text, TouchableOpacity, StyleSheet } from "react-native";

export default function SignupScreen() {
  const [email, setEmail] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = () => {
    if (!email.includes("@")) {
      setError("Please enter a valid email address.");
      return;
    }
    setError("");
  };

  return (
    &lt;View style={styles.container}&gt;
      &lt;TextInput
        style={styles.input}
        placeholder="Email address"
        value={email}
        onChangeText={setEmail}
        keyboardType="email-address"
        autoCapitalize="none"
      /&gt;
      {error ? &lt;Text style={styles.error}&gt;{error}&lt;/Text&gt; : null}
      &lt;TouchableOpacity style={styles.button} onPress={handleSubmit}&gt;
        &lt;Text style={styles.buttonText}&gt;Continue&lt;/Text&gt;
      &lt;/TouchableOpacity&gt;
    &lt;/View&gt;
  );
}

const styles = StyleSheet.create({
  container: { padding: 20 },
  input: { borderWidth: 1, borderColor: "#ccc", borderRadius: 8, padding: 12, marginBottom: 8 },
  error: { color: "red", marginBottom: 8 },
  button: { backgroundColor: "#2563eb", padding: 14, borderRadius: 8, alignItems: "center" },
  buttonText: { color: "white", fontWeight: "bold" },
});</code></pre><h2>Keyboard Types Matter</h2><p>Setting <code>keyboardType="email-address"</code> or <code>keyboardType="numeric"</code> shows the correct keyboard layout, a small detail that professional apps always get right and beginner apps often miss.</p>""",
            "key_concepts": ["TextInput", "controlled inputs", "onChangeText", "form validation", "keyboardType"],
            "practical_exercise": {
                "title": "Build a Validated Signup Form",
                "instructions": "Build a signup screen with TextInput fields for name, email, and password, using state to control each value. Add validation that shows an error message if the email does not contain '@' or the password is under 6 characters. Submit your code and a screen recording showing both the error and success states."
            },
            "quiz": [
                {"question": "What does it mean for a TextInput to be 'controlled'?", "options": ["Its value is driven by component state and updated via onChangeText", "It cannot be edited by the user", "It automatically validates itself", "It only appears on Android"], "correct_index": 0, "explanation": "A controlled input's displayed value comes from state, updated through a handler like onChangeText, keeping the UI in sync with data."},
                {"question": "What does setting keyboardType='numeric' do?", "options": ["Disables the keyboard entirely", "Forces the app to crash on non-numeric input", "Changes the app's color theme", "Shows a keyboard optimized for entering numbers"], "correct_index": 3, "explanation": "keyboardType controls which on-screen keyboard layout appears, improving usability for fields like phone numbers or prices."},
                {"question": "Which prop updates a TextInput's state as the user types?", "options": ["onSubmit", "onChangeText", "onPress", "onFocus"], "correct_index": 1, "explanation": "onChangeText fires on every keystroke, passing the new text value so it can be stored in state."}
            ],
            "resources": [
                {"label": "React Native TextInput", "url": "https://reactnative.dev/docs/textinput"}
            ]
        },
        {
            "day_number": 9,
            "week_number": 2,
            "week_title": "Navigation and Multi-Screen Apps",
            "title": "Persisting Data on the Device with AsyncStorage",
            "learning_objective": "By the end of this class, you will be able to save and retrieve data locally so it survives an app restart.",
            "duration_minutes": 30,
            "content_html": """<p>If you close an app and reopen it, and everything you entered is gone, that app feels broken. Real apps remember things: your login session, your saved items, your settings. AsyncStorage is the standard way to persist small amounts of data locally on the device in React Native.</p><h2>Reading and Writing with AsyncStorage</h2><p>AsyncStorage is a simple, asynchronous key-value store, similar to localStorage on the web but working across both iOS and Android. Every operation returns a Promise, so it is normally used with async/await.</p><pre><code>npx expo install @react-native-async-storage/async-storage

import AsyncStorage from "@react-native-async-storage/async-storage";

const saveTasks = async (tasks) => {
  try {
    await AsyncStorage.setItem("tasks", JSON.stringify(tasks));
  } catch (e) {
    console.error("Failed to save tasks", e);
  }
};

const loadTasks = async () => {
  const json = await AsyncStorage.getItem("tasks");
  return json != null ? JSON.parse(json) : [];
};</code></pre><h2>Loading Saved Data on App Start</h2><p>Data is normally loaded inside a <code>useEffect</code> that runs once when a screen mounts, so the saved data appears immediately when the app opens, rather than the user seeing a blank screen.</p><pre><code>useEffect(() => {
  loadTasks().then(setTasks);
}, []);</code></pre><p>This is the exact mechanism your final project will use to persist real user data locally, one of the required features of that project.</p>""",
            "key_concepts": ["AsyncStorage", "key-value storage", "JSON.stringify/parse", "async/await", "useEffect on mount"],
            "practical_exercise": {
                "title": "Build a Persistent To-Do List",
                "instructions": "Build a to-do list screen where users can add and delete tasks, saving the full list to AsyncStorage on every change and loading it back with useEffect when the app starts. Fully close the app (not just background it) and reopen it to confirm your tasks are still there. Submit your code and a screen recording showing the app closed and reopened with data intact."
            },
            "quiz": [
                {"question": "What does AsyncStorage provide in a React Native app?", "options": ["A remote SQL database", "Simple local key-value storage that persists across app restarts", "A way to send push notifications", "A navigation library"], "correct_index": 1, "explanation": "AsyncStorage is a local, asynchronous key-value store used to persist small amounts of data on the device."},
                {"question": "Why must objects be converted with JSON.stringify before saving to AsyncStorage?", "options": ["AsyncStorage only stores string values", "It is not actually required", "JSON.stringify deletes the data", "AsyncStorage only works with numbers"], "correct_index": 0, "explanation": "AsyncStorage stores only strings, so objects and arrays must be serialized with JSON.stringify before saving and parsed back after loading."},
                {"question": "Where is saved data typically loaded back when a screen first appears?", "options": ["Inside a useEffect that runs on mount", "It loads automatically with no code needed", "Only when the user presses a refresh button", "Inside the StyleSheet"], "correct_index": 0, "explanation": "A useEffect with an empty dependency array runs once when the component mounts, making it the standard place to load persisted data."}
            ],
            "resources": [
                {"label": "React Native Async Storage", "url": "https://reactnative.dev/docs/asyncstorage"}
            ]
        },
        {
            "day_number": 10,
            "week_number": 2,
            "week_title": "Navigation and Multi-Screen Apps",
            "title": "Assembling Your First Complete Multi-Screen App",
            "learning_objective": "By the end of this class, you will be able to combine tabs, forms, lists, and local storage into one cohesive multi-screen app.",
            "duration_minutes": 30,
            "content_html": """<p>You now have every core building block: screens, navigation, lists, forms, and persistence. Today is about combining them into one real, cohesive app rather than isolated exercises, which is the actual skill employers care about, not any single component in isolation.</p><h2>Planning the App Structure</h2><p>Before writing code, sketch your screens and how they connect. A simple habit tracker, for example, needs a Home tab (list of habits), an Add Habit screen (a form, reached via a stack push from Home), and a Profile tab (settings).</p><pre><code>App
 └─ Tab.Navigator
     ├─ HomeStack
     │   ├─ HomeScreen (FlatList of habits)
     │   └─ AddHabitScreen (form, pushed from Home)
     └─ ProfileScreen</code></pre><h2>Wiring It Together</h2><p>Data flows one direction: habits are loaded from AsyncStorage into state in a top-level component (or a shared context), passed down to HomeScreen as props, and updated whenever AddHabitScreen saves a new one, using <code>navigation.goBack()</code> to return to Home after saving.</p><p>This kind of planning-before-coding is what separates developers who ship working apps from those who get stuck halfway through. Practicing it now on a small app prepares you for the more complex API-driven app coming in week three.</p>""",
            "key_concepts": ["app architecture planning", "combining navigators", "data flow between screens", "navigation.goBack()"],
            "practical_exercise": {
                "title": "Build a Habit Tracker App",
                "instructions": "Build a small habit tracker app with a bottom tab navigator containing a Home tab (FlatList of habits, persisted with AsyncStorage) and a Profile tab. From Home, add a button that pushes an Add Habit form screen; on submit, save the new habit and navigate back to Home showing the updated list. Submit your full project code and a screen recording demoing the complete flow."
            },
            "quiz": [
                {"question": "Why is it useful to sketch your screen structure before coding a multi-screen app?", "options": ["It is not useful, code should always come first", "Sketching is required by React Navigation", "It clarifies how screens and navigation connect before you write code, reducing rework", "It replaces the need for testing"], "correct_index": 2, "explanation": "Planning screen structure and data flow before coding helps avoid major restructuring once significant code has been written."},
                {"question": "What does navigation.goBack() do?", "options": ["Deletes the current screen's data permanently", "Restarts the entire app", "Logs the user out", "Returns the user to the previous screen in the navigation stack"], "correct_index": 3, "explanation": "navigation.goBack() pops the current screen off the stack, returning to the previous one, commonly used after a form submits."},
                {"question": "In a habit tracker with a top-level habits list in state, how should a new habit added on one screen reach the list shown on another?", "options": ["By updating the shared state (or AsyncStorage-backed state) that both screens read from", "It cannot be done in React Native", "By manually restarting the app", "Each screen keeps fully separate, unrelated data"], "correct_index": 0, "explanation": "Shared state (often lifted up or in context) updated by one screen and read by another is how data stays in sync across an app."}
            ],
            "resources": [
                {"label": "React Navigation Documentation", "url": "https://reactnavigation.org/docs/getting-started"}
            ]
        },
        {
            "day_number": 11,
            "week_number": 3,
            "week_title": "Connecting to Real Data with APIs",
            "title": "Fetching Live Data from a Public API",
            "learning_objective": "By the end of this class, you will be able to fetch and display live data from a real public API using fetch and useEffect.",
            "duration_minutes": 30,
            "content_html": """<p>Every real app you use pulls live data from a server: weather apps, news apps, delivery apps. Today you connect your app to the outside world for the first time, which is the single biggest step from "tutorial project" to "real app."</p><h2>Fetching Data with useEffect</h2><p>The fetch API works the same in React Native as it does on the web. It is combined with useState to hold the result and useEffect to trigger the request when the screen loads.</p><pre><code>import { useState, useEffect } from "react";
import { View, Text, FlatList, ActivityIndicator } from "react-native";

export default function NewsScreen() {
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("https://jsonplaceholder.typicode.com/posts")
      .then((res) => res.json())
      .then((data) => {
        setArticles(data);
        setLoading(false);
      });
  }, []);

  if (loading) return &lt;ActivityIndicator size="large" style={{ marginTop: 40 }} /&gt;;

  return (
    &lt;FlatList
      data={articles}
      keyExtractor={(item) =&gt; String(item.id)}
      renderItem={({ item }) =&gt; (
        &lt;View style={{ padding: 16 }}&gt;
          &lt;Text style={{ fontWeight: "bold" }}&gt;{item.title}&lt;/Text&gt;
        &lt;/View&gt;
      )}
    /&gt;
  );
}</code></pre><h2>Why Loading State Matters</h2><p>Networks in Nigeria are not always fast, so showing an ActivityIndicator while data loads, rather than a blank screen, is a basic professional standard your final project will be graded on.</p>""",
            "key_concepts": ["fetch API", "useEffect data fetching", "loading state", "ActivityIndicator", "async data flow"],
            "practical_exercise": {
                "title": "Build a Live Data Feed Screen",
                "instructions": "Build a screen that fetches data from a public API of your choice (for example jsonplaceholder.typicode.com or any free API you find) and displays the results in a FlatList, showing an ActivityIndicator while loading. Submit your code and a screenshot of the loaded data on your device."
            },
            "quiz": [
                {"question": "Why should useEffect with an empty dependency array be used for an initial data fetch?", "options": ["It fetches data on every keystroke", "It prevents the app from ever fetching data", "It only works on Android", "It runs the fetch once, when the component first mounts"], "correct_index": 3, "explanation": "An empty dependency array ([]) makes useEffect run exactly once, right after the component mounts, ideal for an initial fetch."},
                {"question": "What is ActivityIndicator used for?", "options": ["Showing a loading spinner while data is being fetched", "Displaying a list of items", "Sending push notifications", "Storing data locally"], "correct_index": 0, "explanation": "ActivityIndicator renders a native loading spinner, commonly shown while waiting for an API response."},
                {"question": "Why is showing a loading state especially important for apps used in Nigeria?", "options": ["It is not important anywhere", "Network conditions can be slow or inconsistent, so users need feedback that something is happening", "Loading states are only cosmetic and never necessary", "It makes the app use less data"], "correct_index": 1, "explanation": "Variable network speeds make clear loading feedback essential so users do not think the app has frozen or crashed."}
            ],
            "resources": [
                {"label": "React Native: Networking", "url": "https://reactnative.dev/docs/network"}
            ]
        },
        {
            "day_number": 12,
            "week_number": 3,
            "week_title": "Connecting to Real Data with APIs",
            "title": "Handling API Errors and Empty States Gracefully",
            "learning_objective": "By the end of this class, you will be able to handle failed API requests and empty results without crashing or confusing the user.",
            "duration_minutes": 25,
            "content_html": """<p>APIs fail. Phones lose signal, servers go down, endpoints return unexpected data. An app that crashes or shows a blank white screen when this happens looks broken and unprofessional; an app that shows a clear, friendly error message looks like it was built by someone who thought about real users.</p><h2>Try/Catch with Fetch</h2><p>Wrapping fetch calls in try/catch, and checking <code>response.ok</code>, catches both network failures and non-200 server responses.</p><pre><code>const [error, setError] = useState(null);

useEffect(() => {
  const loadData = async () => {
    try {
      const response = await fetch("https://api.example.com/items");
      if (!response.ok) throw new Error("Server returned an error");
      const data = await response.json();
      setItems(data);
    } catch (e) {
      setError("Could not load data. Check your connection and try again.");
    } finally {
      setLoading(false);
    }
  };
  loadData();
}, []);</code></pre><h2>Handling the Empty State</h2><p>Separately from errors, a successful request can still return zero results, like a search with no matches. This needs its own message, distinct from an error, such as "No items found" rather than leaving a blank screen the user might mistake for a bug.</p><pre><code>if (error) return &lt;Text&gt;{error}&lt;/Text&gt;;
if (items.length === 0) return &lt;Text&gt;No items found.&lt;/Text&gt;;</code></pre>""",
            "key_concepts": ["try/catch with fetch", "response.ok", "error state", "empty state UI", "finally block"],
            "practical_exercise": {
                "title": "Add Error and Empty State Handling",
                "instructions": "Take your Day 11 API screen and add proper error handling: wrap the fetch in try/catch, show a clear error message if the request fails, and show a distinct 'no results' message for an empty response. Test the error path by temporarily fetching a broken or misspelled URL. Submit your updated code and a screenshot of the error state."
            },
            "quiz": [
                {"question": "Why should fetch calls check response.ok in addition to using try/catch?", "options": ["response.ok is not a real property", "try/catch alone catches every possible failure", "Checking response.ok is only needed on Android", "fetch does not automatically throw an error for HTTP error status codes like 404 or 500"], "correct_index": 3, "explanation": "fetch only rejects on network failure; HTTP error responses (like 404 or 500) still resolve successfully, so response.ok must be checked manually."},
                {"question": "What is the difference between an error state and an empty state?", "options": ["They are the same thing", "An error means the request failed; an empty state means the request succeeded but returned zero results", "An empty state means the app crashed", "Error states should never be shown to users"], "correct_index": 1, "explanation": "An error indicates the request itself failed, while an empty state means the request succeeded but simply found nothing to show."},
                {"question": "What does a finally block guarantee in a try/catch/finally structure?", "options": ["It only runs if there is no error", "It prevents any errors from occurring", "It runs regardless of whether the try block succeeded or the catch block ran", "It runs before the try block"], "correct_index": 2, "explanation": "The finally block always executes after try/catch, regardless of outcome, making it ideal for stopping a loading indicator."}
            ],
            "resources": [
                {"label": "MDN: Using Fetch", "url": "https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch"}
            ]
        },
        {
            "day_number": 13,
            "week_number": 3,
            "week_title": "Connecting to Real Data with APIs",
            "title": "Sending Data to a Server with POST Requests",
            "learning_objective": "By the end of this class, you will be able to send new data to a server using a POST request from a form screen.",
            "duration_minutes": 30,
            "content_html": """<p>So far your app has only read data. Real apps also write data: posting a comment, creating an account, submitting an order. This is done with a POST request, sending data in the request body instead of just asking for it.</p><h2>Sending a POST Request</h2><p>A POST request includes a method, headers describing the data format, and a body containing the actual data, usually JSON.</p><pre><code>const createPost = async (title, body) => {
  try {
    const response = await fetch("https://jsonplaceholder.typicode.com/posts", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title, body, userId: 1 }),
    });
    if (!response.ok) throw new Error("Failed to create post");
    const created = await response.json();
    return created;
  } catch (e) {
    console.error(e);
    throw e;
  }
};</code></pre><h2>Wiring a Form to a POST Request</h2><p>Combine this with what you learned about forms: collect input with TextInput and state, call this function on submit, show a loading state on the button while the request is in flight, and navigate away or show a success message once it completes.</p><pre><code>const handleSubmit = async () => {
  setSubmitting(true);
  await createPost(title, body);
  setSubmitting(false);
  navigation.goBack();
};</code></pre>""",
            "key_concepts": ["POST requests", "request headers", "JSON request body", "Content-Type header", "submit loading state"],
            "practical_exercise": {
                "title": "Build a Create-Post Form",
                "instructions": "Build a form screen with title and body fields that sends a POST request to https://jsonplaceholder.typicode.com/posts when submitted, disabling the submit button and showing a loading indicator while the request is in flight. On success, show the returned created post's id to the user. Submit your code and a screenshot of the success result."
            },
            "quiz": [
                {"question": "What HTTP method is used to send new data to create a resource on a server?", "options": ["GET", "DELETE", "POST", "HEAD"], "correct_index": 2, "explanation": "POST is the standard HTTP method for sending data to a server to create a new resource."},
                {"question": "Why is the Content-Type header set to application/json in a POST request?", "options": ["It is not necessary and can be omitted", "It tells the server the request body is formatted as JSON", "It sets the response language", "It authenticates the user"], "correct_index": 1, "explanation": "The Content-Type header tells the server how to correctly parse the incoming request body."},
                {"question": "Why should a submit button be disabled while a POST request is in flight?", "options": ["It is purely a cosmetic choice with no real benefit", "Disabling buttons is required by React Native and cannot be avoided", "It speeds up the network request", "To prevent the user from accidentally submitting the same data multiple times"], "correct_index": 3, "explanation": "Disabling the button during submission prevents duplicate requests from repeated taps while waiting for a response."}
            ],
            "resources": [
                {"label": "MDN: Fetch POST Requests", "url": "https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch"}
            ]
        },
        {
            "day_number": 14,
            "week_number": 3,
            "week_title": "Connecting to Real Data with APIs",
            "title": "Managing Shared State Across Screens with Context",
            "learning_objective": "By the end of this class, you will be able to share state like a logged-in user across multiple screens using React Context.",
            "duration_minutes": 30,
            "content_html": """<p>As an app grows past a few screens, passing data down through props alone becomes painful, especially for data like a logged-in user or theme setting that many unrelated screens need. React Context solves this by letting any screen or component read shared state directly.</p><h2>Creating a Context</h2><p>A Context is created once, provided at the top of the app, and consumed anywhere below it in the component tree without manually passing props through every level.</p><pre><code>import { createContext, useContext, useState } from "react";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  return (
    &lt;AuthContext.Provider value={{ user, setUser }}&gt;
      {children}
    &lt;/AuthContext.Provider&gt;
  );
}

export function useAuth() {
  return useContext(AuthContext);
}</code></pre><h2>Using Context in Any Screen</h2><p>Wrap your NavigationContainer with the provider, then any screen can call <code>useAuth()</code> to read or update the shared user, without it being passed as a prop through every intermediate screen.</p><pre><code>function ProfileScreen() {
  const { user, setUser } = useAuth();
  return &lt;Text&gt;Welcome, {user?.name}&lt;/Text&gt;;
}</code></pre><p>This is the standard pattern real apps use for auth state, and it will make your final project's screens far cleaner than passing data manually everywhere.</p>""",
            "key_concepts": ["React Context", "createContext", "useContext", "Provider pattern", "shared app state"],
            "practical_exercise": {
                "title": "Build a Shared Auth Context",
                "instructions": "Create an AuthContext with a fake login function that sets a user object in state, wrap your app in the AuthProvider, and build two screens (a Login screen and a Profile screen) that both use useAuth() to read or set the current user without passing props manually. Submit your code and a screen recording showing login state reflected on the Profile screen."
            },
            "quiz": [
                {"question": "What problem does React Context solve?", "options": ["It fetches data from APIs", "It lets components access shared state without passing props through every level", "It replaces the need for navigation", "It stores data permanently on the device"], "correct_index": 1, "explanation": "Context avoids 'prop drilling' by letting any nested component read shared state directly via useContext."},
                {"question": "What hook is used to read a value from a Context inside a component?", "options": ["useState", "useEffect", "useContext", "useNavigation"], "correct_index": 2, "explanation": "useContext(SomeContext) lets a component read the current value provided by that Context's Provider."},
                {"question": "Where must a Context's Provider typically be placed to make its value available to the whole app?", "options": ["Inside every individual screen separately", "Near the top of the component tree, wrapping the screens that need it", "It does not matter where it is placed", "Only inside the final screen"], "correct_index": 1, "explanation": "Wrapping the app (often around the navigator) with the Provider makes the shared value available to all nested screens."}
            ],
            "resources": [
                {"label": "React Context Documentation", "url": "https://react.dev/reference/react/useContext"}
            ]
        },
        {
            "day_number": 15,
            "week_number": 3,
            "week_title": "Connecting to Real Data with APIs",
            "title": "Building a Complete API-Driven Screen: A Mini Case Study",
            "learning_objective": "By the end of this class, you will be able to build a complete screen that fetches, displays, searches, and refreshes real API data.",
            "duration_minutes": 35,
            "content_html": """<p>Today combines everything from week three into one realistic screen: a searchable, refreshable list backed by a live API, the exact pattern behind apps like a job board, a restaurant finder, or a marketplace listings page.</p><h2>Adding Search with a Controlled Input</h2><p>Filtering a fetched list is usually done client-side, by filtering the already-loaded array based on a TextInput's value, rather than making a new API call on every keystroke.</p><pre><code>const [query, setQuery] = useState("");
const filtered = items.filter((item) =&gt;
  item.title.toLowerCase().includes(query.toLowerCase())
);</code></pre><h2>Adding Pull-to-Refresh</h2><p>FlatList has built-in support for the pull-to-refresh gesture users expect from every modern app, using the <code>refreshing</code> and <code>onRefresh</code> props.</p><pre><code>const [refreshing, setRefreshing] = useState(false);

const onRefresh = async () => {
  setRefreshing(true);
  await fetchItems();
  setRefreshing(false);
};

&lt;FlatList
  data={filtered}
  refreshing={refreshing}
  onRefresh={onRefresh}
  renderItem={renderItem}
  keyExtractor={(item) =&gt; String(item.id)}
/&gt;</code></pre><h2>Case Study: A Real Job Board Screen</h2><p>Picture a campus job board app: it fetches listings on load, lets students search by keyword, and supports pull-to-refresh to check for new postings. That is precisely today's exercise, and it is a legitimate, demoable feature set on its own.</p>""",
            "key_concepts": ["client-side search/filter", "pull-to-refresh", "refreshing/onRefresh props", "combining fetch, state, and lists"],
            "practical_exercise": {
                "title": "Build a Searchable, Refreshable Listings Screen",
                "instructions": "Extend your API-connected FlatList screen from earlier this week with a search TextInput that filters results client-side, and pull-to-refresh support that re-fetches the data. Test both features on your device. Submit your code and a screen recording demonstrating search and pull-to-refresh."
            },
            "quiz": [
                {"question": "Why is client-side filtering typically used for a search box over an already-fetched list?", "options": ["It is impossible to filter data any other way", "It avoids making a new network request on every keystroke, keeping search instant", "Client-side filtering is required by FlatList", "APIs cannot support search parameters"], "correct_index": 1, "explanation": "Filtering already-loaded data locally is fast and avoids excessive network requests compared to hitting the API on every keystroke."},
                {"question": "Which two FlatList props enable the pull-to-refresh gesture?", "options": ["refreshing and onRefresh", "data and keyExtractor", "renderItem and style", "loading and error"], "correct_index": 0, "explanation": "refreshing (a boolean) and onRefresh (a callback) together enable and control FlatList's built-in pull-to-refresh behavior."},
                {"question": "In the job board case study, what two features were combined to make the screen realistic?", "options": ["Push notifications and payments", "Dark mode and animations", "Search filtering and pull-to-refresh on live API data", "Offline mode and biometric login"], "correct_index": 2, "explanation": "The case study combined a searchable list with pull-to-refresh over live API data, a common realistic feature combination."}
            ],
            "resources": [
                {"label": "React Native FlatList", "url": "https://reactnative.dev/docs/flatlist"}
            ]
        },
        {
            "day_number": 16,
            "week_number": 4,
            "week_title": "Polishing Real Apps: UX, Media, and Device Features",
            "title": "Designing Mobile UI That Does Not Look Like a Tutorial Project",
            "learning_objective": "By the end of this class, you will be able to apply consistent spacing, typography, and color to make a screen look professionally designed.",
            "duration_minutes": 25,
            "content_html": """<p>Two apps with identical functionality can look completely different in quality, and design is often the first thing a recruiter, client, or app store reviewer judges. Consistent visual rules, not artistic talent, are what separate a tutorial-looking app from a professional one.</p><h2>A Simple Design System: Spacing and Color Constants</h2><p>Instead of hardcoding random pixel values and colors throughout your app, define them once in a shared file and reuse them everywhere, guaranteeing visual consistency.</p><pre><code>// theme.js
export const colors = {
  primary: "#2563eb",
  background: "#f9fafb",
  text: "#111827",
  muted: "#6b7280",
  danger: "#dc2626",
};

export const spacing = { sm: 8, md: 16, lg: 24, xl: 32 };</code></pre><h2>Applying It Consistently</h2><pre><code>import { colors, spacing } from "../theme";

const styles = StyleSheet.create({
  card: {
    backgroundColor: "white",
    padding: spacing.md,
    borderRadius: 12,
    marginBottom: spacing.sm,
    shadowColor: "#000",
    shadowOpacity: 0.05,
    shadowRadius: 8,
    elevation: 2,
  },
  title: { fontSize: 18, fontWeight: "600", color: colors.text },
});</code></pre><p>Reusing a small palette and spacing scale across every screen, rather than picking new values each time, is the single highest-leverage change you can make to how professional your app looks by day 30.</p>""",
            "key_concepts": ["design consistency", "theme/spacing constants", "shadow and elevation", "typography hierarchy"],
            "practical_exercise": {
                "title": "Create and Apply a Theme File",
                "instructions": "Create a theme.js file defining a color palette and spacing scale, then apply it consistently to restyle at least two existing screens from earlier days so they share the same visual language. Submit your theme.js file and before/after screenshots of one restyled screen."
            },
            "quiz": [
                {"question": "Why define colors and spacing as shared constants instead of hardcoding values in each screen?", "options": ["It makes the app slower", "It ensures visual consistency and makes future design changes easier to apply everywhere", "React Native requires it", "It has no real benefit"], "correct_index": 1, "explanation": "Centralizing design values keeps the app visually consistent and means updating one value in a theme file updates every screen using it."},
                {"question": "What is often the first thing a recruiter or reviewer judges about an app?", "options": ["The backend framework used", "The visual design and polish", "The programming language", "The number of git commits"], "correct_index": 1, "explanation": "Visual polish is usually the first impression an app makes, even before functionality is tested."},
                {"question": "On Android, which style property is commonly used alongside shadow properties to create a card shadow effect?", "options": ["elevation", "opacity", "zIndex", "fontWeight"], "correct_index": 0, "explanation": "Android uses the elevation property to render shadows, while iOS uses shadowColor/shadowOpacity/shadowRadius; both are often set together."}
            ],
            "resources": [
                {"label": "React Native Style Documentation", "url": "https://reactnative.dev/docs/style"}
            ]
        },
        {
            "day_number": 17,
            "week_number": 4,
            "week_title": "Polishing Real Apps: UX, Media, and Device Features",
            "title": "Using the Camera and Image Picker for User-Generated Content",
            "learning_objective": "By the end of this class, you will be able to let a user pick or capture an image and display it in the app.",
            "duration_minutes": 30,
            "content_html": """<p>Profile pictures, marketplace listing photos, receipt scans: a huge number of real apps let users add their own images. This requires accessing device hardware, which is one of the clearest examples of what a native app can do that a plain website cannot do as smoothly.</p><h2>Requesting Permission and Picking an Image</h2><p>Accessing the camera or photo library requires the user's permission, which Expo's ImagePicker handles for you, prompting the OS-level permission dialog automatically.</p><pre><code>npx expo install expo-image-picker

import * as ImagePicker from "expo-image-picker";
import { useState } from "react";
import { View, Image, Button } from "react-native";

export default function AvatarPicker() {
  const [image, setImage] = useState(null);

  const pickImage = async () => {
    const permission = await ImagePicker.requestMediaLibraryPermissionsAsync();
    if (!permission.granted) return;

    const result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      quality: 0.7,
    });

    if (!result.canceled) {
      setImage(result.assets[0].uri);
    }
  };

  return (
    &lt;View&gt;
      &lt;Button title="Choose Photo" onPress={pickImage} /&gt;
      {image &amp;&amp; &lt;Image source={{ uri: image }} style={{ width: 150, height: 150 }} /&gt;}
    &lt;/View&gt;
  );
}</code></pre><h2>Why Permissions Matter</h2><p>Always check whether permission was actually granted before proceeding, and handle the denied case gracefully with a message rather than a silent failure or crash, since app store review processes specifically check for this.</p>""",
            "key_concepts": ["expo-image-picker", "requesting device permissions", "launchImageLibraryAsync", "handling denied permissions"],
            "practical_exercise": {
                "title": "Build a Profile Photo Picker",
                "instructions": "Add an image picker to a profile screen that requests media library permission, lets the user choose a photo, and displays it in a circular avatar. Handle the case where the user denies permission by showing a clear message instead of failing silently. Submit your code and a screenshot showing a selected image."
            },
            "quiz": [
                {"question": "Why must an app request permission before accessing the photo library or camera?", "options": ["It is optional and can be skipped", "Mobile operating systems require explicit user consent to protect user privacy", "Permissions only apply to paid apps", "It is only required on Android, never iOS"], "correct_index": 1, "explanation": "Both iOS and Android require apps to request explicit user permission before accessing sensitive resources like the camera or photo library."},
                {"question": "What should happen if a user denies the requested permission?", "options": ["The app should crash", "The app should ignore it and try to access the photos anyway", "The app should show a clear message rather than failing silently", "Nothing needs to be handled"], "correct_index": 2, "explanation": "Gracefully handling denied permissions with a clear message is expected professional behavior and required by app store review."},
                {"question": "Which Expo package is used to let users pick images from their photo library?", "options": ["expo-camera", "expo-file-system", "expo-notifications", "expo-image-picker"], "correct_index": 3, "explanation": "expo-image-picker provides functions like launchImageLibraryAsync to let users select or capture images."}
            ],
            "resources": [
                {"label": "Expo Image Picker", "url": "https://docs.expo.dev/versions/latest/sdk/imagepicker/"}
            ]
        },
        {
            "day_number": 18,
            "week_number": 4,
            "week_title": "Polishing Real Apps: UX, Media, and Device Features",
            "title": "Using Device Location for Location-Aware Features",
            "learning_objective": "By the end of this class, you will be able to request and use the device's GPS location in an app.",
            "duration_minutes": 25,
            "content_html": """<p>Delivery apps, ride-hailing apps, and local business finders all rely on knowing where the user is. Location access is another native device capability, and handling it correctly, including denial and inaccurate results, is a mark of a careful mobile developer.</p><h2>Requesting Location Permission and Reading Coordinates</h2><pre><code>npx expo install expo-location

import * as Location from "expo-location";
import { useState, useEffect } from "react";
import { Text, View } from "react-native";

export default function NearbyScreen() {
  const [location, setLocation] = useState(null);
  const [errorMsg, setErrorMsg] = useState(null);

  useEffect(() => {
    (async () => {
      const { status } = await Location.requestForegroundPermissionsAsync();
      if (status !== "granted") {
        setErrorMsg("Location permission was denied.");
        return;
      }
      const loc = await Location.getCurrentPositionAsync({});
      setLocation(loc.coords);
    })();
  }, []);

  if (errorMsg) return &lt;Text&gt;{errorMsg}&lt;/Text&gt;;
  if (!location) return &lt;Text&gt;Getting your location...&lt;/Text&gt;;

  return (
    &lt;View&gt;
      &lt;Text&gt;Latitude: {location.latitude}&lt;/Text&gt;
      &lt;Text&gt;Longitude: {location.longitude}&lt;/Text&gt;
    &lt;/View&gt;
  );
}</code></pre><h2>Real-World Use: Nearby Filtering</h2><p>Once you have coordinates, a real app typically sends them to an API or compares them against a list of known locations to show "nearby" results, exactly the pattern behind food delivery apps showing restaurants close to you.</p>""",
            "key_concepts": ["expo-location", "requestForegroundPermissionsAsync", "getCurrentPositionAsync", "location-based features"],
            "practical_exercise": {
                "title": "Build a Location Display Screen",
                "instructions": "Build a screen that requests location permission and displays the device's current latitude and longitude, handling both the denied-permission case and the loading case with clear messages. Test it on a real device (location does not work reliably in most simulators). Submit your code and a screenshot of the result."
            },
            "quiz": [
                {"question": "What must an app do before reading the device's GPS coordinates?", "options": ["Nothing, location is available by default", "Request foreground location permission from the user", "Pay for an Expo subscription", "Only Android requires a permission request"], "correct_index": 1, "explanation": "Location access requires explicit permission via requestForegroundPermissionsAsync before coordinates can be read."},
                {"question": "Which Expo function retrieves the device's current GPS coordinates?", "options": ["Location.getCurrentPositionAsync", "Location.requestForegroundPermissionsAsync", "ImagePicker.launchImageLibraryAsync", "AsyncStorage.getItem"], "correct_index": 0, "explanation": "getCurrentPositionAsync returns the device's current coordinates once permission has been granted."},
                {"question": "Why is it recommended to test location features on a real device rather than a simulator?", "options": ["Simulators cannot run React Native apps at all", "Simulated location is often inaccurate or requires manual configuration, unlike a real device's GPS", "Real devices are always faster", "Simulators do not support Expo"], "correct_index": 1, "explanation": "Simulators typically use a fixed or manually set mock location, so testing on a real device gives more reliable, realistic GPS behavior."}
            ],
            "resources": [
                {"label": "Expo Location", "url": "https://docs.expo.dev/versions/latest/sdk/location/"}
            ]
        },
        {
            "day_number": 19,
            "week_number": 4,
            "week_title": "Polishing Real Apps: UX, Media, and Device Features",
            "title": "Adding Confirmations, Alerts, and Feedback Users Trust",
            "learning_objective": "By the end of this class, you will be able to add native alerts, confirmations, and toast-style feedback for destructive or important actions.",
            "duration_minutes": 20,
            "content_html": """<p>Deleting a saved item, logging out, or submitting a payment should never happen from a single accidental tap. Confirmations and feedback build user trust, and their absence is one of the fastest ways an app feels unfinished or risky to use.</p><h2>Confirming Destructive Actions with Alert</h2><p>React Native's built-in Alert API shows a native platform dialog, which feels far more trustworthy to users than a custom-built popup.</p><pre><code>import { Alert } from "react-native";

const confirmDelete = (id, onConfirm) => {
  Alert.alert(
    "Delete this item?",
    "This action cannot be undone.",
    [
      { text: "Cancel", style: "cancel" },
      { text: "Delete", style: "destructive", onPress: () =&gt; onConfirm(id) },
    ]
  );
};</code></pre><h2>Giving Feedback After an Action</h2><p>After a successful action, like saving a form, users need confirmation it worked, whether through a brief Alert, a temporary success message, or navigating them to a new screen. Silence after an important action leaves users unsure whether anything happened, and they may tap the button again, causing duplicate actions.</p><pre><code>Alert.alert("Saved", "Your changes have been saved successfully.");</code></pre>""",
            "key_concepts": ["Alert API", "destructive action confirmation", "user feedback patterns", "avoiding silent failures"],
            "practical_exercise": {
                "title": "Add Delete Confirmations to Your App",
                "instructions": "Go back to an app you built earlier (such as the habit tracker or to-do list) and add an Alert confirmation before any delete action, plus a success Alert or message after a save action completes. Submit your updated code and a screen recording showing the confirmation dialog in action."
            },
            "quiz": [
                {"question": "Why should destructive actions like deleting data require a confirmation step?", "options": ["Confirmations are only for decoration", "To prevent accidental data loss from a single unintended tap", "It is a legal requirement in every country", "Users prefer more taps regardless of purpose"], "correct_index": 1, "explanation": "A confirmation step protects users from accidentally losing data through a single accidental tap, especially for irreversible actions."},
                {"question": "What does React Native's Alert.alert() display?", "options": ["A custom HTML modal", "A push notification", "A new screen via navigation", "A native platform confirmation or information dialog"], "correct_index": 3, "explanation": "Alert.alert() renders the operating system's native dialog UI, which feels familiar and trustworthy to users."},
                {"question": "What can happen if an app gives no feedback after a user submits an important action?", "options": ["Nothing, users always assume success", "The app automatically shows feedback regardless", "The user may not know it worked and could tap the button again, risking a duplicate action", "It has no real consequence"], "correct_index": 2, "explanation": "Without clear feedback, users may be unsure the action succeeded and repeat it, potentially causing duplicate submissions."}
            ],
            "resources": [
                {"label": "React Native Alert", "url": "https://reactnative.dev/docs/alert"}
            ]
        },
        {
            "day_number": 20,
            "week_number": 4,
            "week_title": "Polishing Real Apps: UX, Media, and Device Features",
            "title": "Case Study: Rebuilding a Feature from a Real Nigerian App",
            "learning_objective": "By the end of this class, you will be able to break down a real app feature into its component parts and rebuild a simplified version.",
            "duration_minutes": 30,
            "content_html": """<p>The fastest way to level up as a mobile developer is studying real apps you already use and asking "how would I build that?" Today you apply everything from weeks one to four by reverse-engineering one feature from a familiar Nigerian app.</p><h2>Breaking Down a Feature: An Order Tracking Screen</h2><p>Consider a food delivery app's order tracking screen. It combines: a FlatList or fixed set of status steps, conditional styling based on current status, live-feeling data (often polled or fetched), and a persistent "current order" saved locally so it survives app restarts.</p><pre><code>const steps = ["Order placed", "Preparing", "Out for delivery", "Delivered"];
const currentStep = 2;

steps.map((step, index) =&gt; (
  &lt;Text
    key={step}
    style={{ color: index &lt;= currentStep ? colors.primary : colors.muted, fontWeight: index === currentStep ? "bold" : "normal" }}
  &gt;
    {step}
  &lt;/Text&gt;
));</code></pre><h2>Why This Exercise Matters</h2><p>Being able to look at a finished feature and mentally decompose it into components, state, and data flow is exactly the skill senior developers use daily, and it is different from following a tutorial step by step. This case-study habit should continue well past this 30-day track.</p>""",
            "key_concepts": ["feature decomposition", "conditional styling", "status/stepper UI pattern", "reverse-engineering real apps"],
            "practical_exercise": {
                "title": "Rebuild One Feature from a Real App",
                "instructions": "Pick one specific feature from a real app you use often (an order tracker, a wallet balance card, a filter/sort menu, or similar), and rebuild a simplified working version of it in React Native using AsyncStorage or local state for its data. Write two to three sentences explaining which real app and feature you chose and what you simplified. Submit your code, your explanation, and a screenshot."
            },
            "quiz": [
                {"question": "What is the main learning goal of reverse-engineering a real app feature?", "options": ["Copying an app's exact source code", "Practicing the skill of decomposing a finished feature into components, state, and data flow", "Learning to design app icons", "Memorizing every screen of a popular app"], "correct_index": 1, "explanation": "Breaking down a real feature into its underlying components and logic builds the analytical skill developers use daily on real projects."},
                {"question": "In the order tracking example, what determines each step's text color and weight?", "options": ["A random number", "The device's battery level", "Whether the step's index is at or before the currentStep value", "The time of day"], "correct_index": 2, "explanation": "The example conditionally styles each step based on comparing its index to currentStep, highlighting completed and active steps."},
                {"question": "Why is this kind of feature-decomposition practice considered different from following a tutorial?", "options": ["It requires independently analyzing and rebuilding a feature without step-by-step instructions", "It is exactly the same as following a tutorial", "Tutorials are always harder than this exercise", "There is no meaningful difference"], "correct_index": 0, "explanation": "Unlike a guided tutorial, this exercise requires independent analysis and decision-making, closer to real on-the-job problem solving."}
            ],
            "resources": []
        },
        {
            "day_number": 21,
            "week_number": 5,
            "week_title": "Production-Ready Practices",
            "title": "Debugging React Native Apps Like a Professional",
            "learning_objective": "By the end of this class, you will be able to use developer tools and structured debugging to diagnose a broken screen.",
            "duration_minutes": 25,
            "content_html": """<p>Every developer, junior or senior, spends real time debugging. What separates a productive developer from a stuck one is not avoiding bugs, it is having a systematic process for finding them quickly, which is also exactly what interviewers probe for in live coding rounds.</p><h2>Reading Error Messages and Using console.log Strategically</h2><p>React Native error screens usually point to the exact file and line. Resist the urge to guess randomly; instead, add targeted console.log statements around the suspected area to confirm what data actually looks like at that point.</p><pre><code>console.log("fetched data:", JSON.stringify(data, null, 2));
console.log("current state before update:", items);</code></pre><h2>Using React Native Debugger Tools</h2><p>Expo apps support remote debugging and the built-in developer menu (shake the device or press <code>m</code> in the terminal), giving access to element inspection and performance monitors, similar to browser DevTools on the web.</p><h2>A Repeatable Debugging Process</h2><p>1) Read the exact error message and line number. 2) Reproduce it reliably. 3) Add logs to narrow down where behavior diverges from expectation. 4) Fix the smallest possible cause. 5) Confirm the fix and remove debug logs. This process works whether the bug is in your own code or a library.</p>""",
            "key_concepts": ["reading stack traces", "strategic console.log", "React Native developer menu", "systematic debugging process"],
            "practical_exercise": {
                "title": "Debug and Document a Real Bug",
                "instructions": "Intentionally introduce a bug into one of your earlier apps (for example, misspell a state variable or break a keyExtractor), then use the five-step debugging process to find and fix it, keeping a short log of what you tried at each step. Submit your before/after code and your debugging log."
            },
            "quiz": [
                {"question": "What is the recommended first step when facing an error in a React Native app?", "options": ["Read the exact error message and identify the file and line it points to", "Immediately rewrite the entire file", "Ignore it and restart the app repeatedly", "Delete the component entirely"], "correct_index": 0, "explanation": "Carefully reading the error message and its location is the fastest way to start narrowing down the actual cause of a bug."},
                {"question": "What is a good use of console.log while debugging?", "options": ["Logging random unrelated values", "Logging the actual data or state at a specific point to confirm it matches expectations", "console.log should never be used in React Native", "Only logging after the bug is already fixed"], "correct_index": 1, "explanation": "Strategic logging of actual values at key points helps confirm exactly where behavior diverges from what was expected."},
                {"question": "How do you typically open the React Native developer menu on a device running via Expo?", "options": ["It cannot be opened on a physical device", "By uninstalling and reinstalling the app", "By shaking the device or pressing a key like 'm' in the terminal", "By turning off Wi-Fi"], "correct_index": 2, "explanation": "Shaking the physical device (or a terminal shortcut) opens Expo's developer menu with debugging and inspection tools."}
            ],
            "resources": [
                {"label": "React Native Debugging", "url": "https://reactnative.dev/docs/debugging"}
            ]
        },
        {
            "day_number": 22,
            "week_number": 5,
            "week_title": "Production-Ready Practices",
            "title": "Structuring a React Native Project for Growth",
            "learning_objective": "By the end of this class, you will be able to organize a growing app's files into a clean, scalable folder structure.",
            "duration_minutes": 25,
            "content_html": """<p>A single App.js file with everything crammed inside works for a five-day exercise, but not for a real app or a job. Employers and code reviewers judge project structure almost as much as functionality, because a messy codebase is expensive to maintain.</p><h2>A Standard Folder Structure</h2><pre><code>my-app/
  screens/
    HomeScreen.js
    ProfileScreen.js
    LoginScreen.js
  components/
    Card.js
    Button.js
  context/
    AuthContext.js
  services/
    api.js
  theme.js
  App.js</code></pre><h2>Separating Concerns: An API Service Layer</h2><p>Instead of writing fetch calls directly inside components, centralize them in a services file, so screens call clean functions and API details live in one place, making it far easier to change an endpoint later.</p><pre><code>// services/api.js
const BASE_URL = "https://jsonplaceholder.typicode.com";

export async function getPosts() {
  const res = await fetch(`${BASE_URL}/posts`);
  if (!res.ok) throw new Error("Failed to fetch posts");
  return res.json();
}</code></pre><p>This structure is what your final project will follow, and it is the same shape you will encounter joining any real production React Native codebase.</p>""",
            "key_concepts": ["folder structure", "separation of concerns", "API service layer", "scalable project organization"],
            "practical_exercise": {
                "title": "Refactor an App into a Clean Structure",
                "instructions": "Take one of your earlier multi-file apps and reorganize it into screens/, components/, and services/ folders, moving any inline fetch calls into a dedicated services/api.js file with named exported functions. Confirm the app still runs correctly after the refactor. Submit your restructured project and a brief note on what you moved."
            },
            "quiz": [
                {"question": "Why does project structure matter to employers reviewing code?", "options": ["It does not matter at all", "A clean, organized structure signals maintainability and professional habits", "Employers only look at the app's icon", "File structure has no relationship to code quality"], "correct_index": 1, "explanation": "Well-organized code is easier to maintain and review, and structure is often one of the first things a reviewer notices."},
                {"question": "What is the benefit of centralizing API calls in a services/api.js file?", "options": ["It makes the app slower", "API logic lives in one place, making endpoints easier to change and reuse across screens", "It is required by React Native and cannot be skipped", "It removes the need for error handling"], "correct_index": 1, "explanation": "A dedicated service layer keeps API logic out of components, making it reusable and easier to update in one place."},
                {"question": "In the standard folder structure shown, where would a reusable Button component typically live?", "options": ["screens/", "context/", "components/", "services/"], "correct_index": 2, "explanation": "Reusable UI pieces like buttons or cards typically live in a components/ folder, separate from full screens."}
            ],
            "resources": [
                {"label": "React Native Documentation", "url": "https://reactnative.dev/docs/getting-started"}
            ]
        },
        {
            "day_number": 23,
            "week_number": 5,
            "week_title": "Production-Ready Practices",
            "title": "Testing Your App Across Devices and Screen Sizes",
            "learning_objective": "By the end of this class, you will be able to test and fix layout issues across different screen sizes and both platforms.",
            "duration_minutes": 25,
            "content_html": """<p>Nigerian users run apps on an enormous range of devices, from budget Android phones with small screens to newer iPhones with notches and rounded corners. An app that only looks right on the exact phone you developed on is not actually finished.</p><h2>Handling Different Screen Sizes</h2><p>Avoid fixed pixel widths for layout; use Flexbox proportions and percentage-based widths instead so layouts adapt naturally.</p><pre><code>// Fragile: breaks on smaller screens
&lt;View style={{ width: 320 }} /&gt;

// Better: adapts to any screen
&lt;View style={{ flex: 1, paddingHorizontal: 16 }} /&gt;</code></pre><h2>Handling Safe Areas</h2><p>Modern phones have notches, camera cutouts, and rounded corners. SafeAreaView (or the react-native-safe-area-context library) keeps your content from being hidden behind these elements.</p><pre><code>import { SafeAreaView } from "react-native-safe-area-context";

export default function Screen() {
  return (
    &lt;SafeAreaView style={{ flex: 1 }}&gt;
      {/* content stays clear of notches and status bars */}
    &lt;/SafeAreaView&gt;
  );
}</code></pre><h2>Testing on Both Platforms</h2><p>Even with one React Native codebase, always test on both an Android and an iOS device or simulator before considering a feature done, since small differences in default styling (like shadows or fonts) do exist between platforms.</p>""",
            "key_concepts": ["responsive layout", "SafeAreaView", "cross-platform testing", "flex-based sizing"],
            "practical_exercise": {
                "title": "Audit and Fix Responsive Issues",
                "instructions": "Take an existing screen from your project and replace any fixed pixel widths with flex or percentage-based sizing, and wrap it in SafeAreaView if it is not already. Test the screen on at least two different device sizes or simulators (or resize the Expo web preview) and note any issues you fixed. Submit your updated code and before/after screenshots."
            },
            "quiz": [
                {"question": "Why is a fixed pixel width like width: 320 risky for layout?", "options": ["It can break or look wrong on screens narrower or wider than that exact value", "It is always the safest option", "React Native does not support fixed widths", "It only affects background colors"], "correct_index": 0, "explanation": "Fixed pixel widths do not adapt to different screen sizes, unlike flex-based or percentage-based sizing."},
                {"question": "What does SafeAreaView help protect content from?", "options": ["Network errors", "Slow API responses", "AsyncStorage failures", "Being hidden behind notches, camera cutouts, and rounded screen corners"], "correct_index": 3, "explanation": "SafeAreaView keeps content within the visible safe area, avoiding overlap with notches, status bars, and rounded corners."},
                {"question": "Why should a feature be tested on both Android and iOS even with a single React Native codebase?", "options": ["It is unnecessary since the code is identical", "Small platform differences in default styling and behavior can still appear", "iOS and Android require completely separate codebases in React Native", "Testing on both is only needed for paid apps"], "correct_index": 1, "explanation": "Despite sharing one codebase, subtle platform differences (shadows, fonts, safe areas) mean both platforms should be checked."}
            ],
            "resources": [
                {"label": "React Native: SafeAreaView", "url": "https://reactnative.dev/docs/safeareaview"}
            ]
        },
        {
            "day_number": 24,
            "week_number": 5,
            "week_title": "Production-Ready Practices",
            "title": "Preparing an App for App Store and Play Store Submission",
            "learning_objective": "By the end of this class, you will be able to explain the steps required to build and submit a React Native app for store release.",
            "duration_minutes": 30,
            "content_html": """<p>Building an app is only half the job; getting it in front of real users means going through the App Store or Play Store submission process, which has its own rules, assets, and review standards that many self-taught developers never learn.</p><h2>Building with EAS</h2><p>Expo Application Services (EAS) builds a real installable binary (.apk/.aab for Android, .ipa for iOS) from your Expo project, without needing a Mac for Android builds.</p><pre><code>npm install -g eas-cli
eas login
eas build:configure
eas build --platform android</code></pre><h2>Store Requirements You Cannot Skip</h2><p>Both stores require: an app icon and splash screen, a privacy policy URL if you collect any user data, screenshots of the app in use, and a clear description. Google Play review is typically faster and cheaper (a one-time $25 fee) than Apple's App Store ($99/year plus a stricter review), which is why many Nigerian indie developers launch on Android first.</p><pre><code>eas submit --platform android</code></pre><h2>What a Hiring Manager Cares About Here</h2><p>Even if you never publish to a store, understanding this pipeline and being able to speak to it in an interview signals you understand the full lifecycle of shipping a mobile app, not just writing screens.</p>""",
            "key_concepts": ["EAS Build", "app store requirements", "app icon/splash screen", "privacy policy", "store review process"],
            "practical_exercise": {
                "title": "Prepare Your Store Submission Assets",
                "instructions": "For one of your existing apps, create an app icon (1024x1024) and a splash screen image, write a two to three sentence store description, and list what a privacy policy for your app would need to disclose given the permissions it uses (camera, location, etc). Submit your icon, splash screen, description, and privacy notes."
            },
            "quiz": [
                {"question": "What does EAS Build produce from an Expo project?", "options": ["A website deployment", "A database backup", "An installable native app binary for Android or iOS", "A Figma design file"], "correct_index": 2, "explanation": "EAS Build compiles a real installable binary (.apk/.aab or .ipa) from an Expo project, ready for testing or store submission."},
                {"question": "Which store submission generally has a lower cost and faster review process?", "options": ["Google Play Store", "Apple App Store", "Both are identical in cost and speed", "Neither charges any fee"], "correct_index": 0, "explanation": "Google Play has a one-time $25 developer fee and typically faster review, compared to Apple's $99/year fee and stricter review process."},
                {"question": "When is a privacy policy URL required for a store submission?", "options": ["Never, it is optional for all apps", "When the app collects any user data, such as through camera or location access", "Only for apps with more than one million downloads", "Only for free apps"], "correct_index": 1, "explanation": "Both app stores require a privacy policy when an app collects user data, including through permissions like camera or location."}
            ],
            "resources": [
                {"label": "Expo Application Services (EAS)", "url": "https://docs.expo.dev/eas/"}
            ]
        },
        {
            "day_number": 25,
            "week_number": 5,
            "week_title": "Production-Ready Practices",
            "title": "What Mobile Developer Job Postings and Interviews Actually Look For",
            "learning_objective": "By the end of this class, you will be able to identify the core skills mobile developer job postings ask for and prepare talking points for an interview.",
            "duration_minutes": 25,
            "content_html": """<p>Knowing how to build screens is necessary but not sufficient to get hired. Understanding exactly what employers screen for lets you present your existing work in the language they expect, which matters as much as the code itself.</p><h2>What Junior Mobile Developer Postings Commonly Require</h2><p>Real Nigerian and remote job postings for junior React Native roles typically list: comfort with React Native or Flutter, REST API integration experience, state management, Git/GitHub usage, and "a portfolio or GitHub showing real projects." Notice that a working app, not a certificate, is usually the actual bar.</p><h2>A Common Interview Question</h2><p><strong>"Walk me through how you would fetch data from an API and display it in a list, handling errors."</strong> A strong answer references exactly what you built in weeks 3-4: useEffect for the fetch, useState for data/loading/error, FlatList for rendering, and try/catch with response.ok checks.</p><h2>Preparing Your Talking Points</h2><p>For each app you have built this month, be ready to explain in two sentences: what problem it solves, and one specific technical decision you made (why you used Context, why you chose FlatList over a plain map, etc). This is exactly what interviewers listen for beyond "does the code work."</p>""",
            "key_concepts": ["junior developer job requirements", "portfolio over certificates", "common interview questions", "explaining technical decisions"],
            "practical_exercise": {
                "title": "Find and Analyze a Real Job Posting",
                "instructions": "Search for one real junior or entry-level React Native or mobile developer job posting (Nigerian or remote), and list every technical requirement it mentions. For each requirement, note which of your apps from this track already demonstrates it. Submit the job posting link/text and your requirement-by-requirement mapping."
            },
            "quiz": [
                {"question": "What do many junior React Native job postings list as proof of skill?", "options": ["A university degree only", "A typing speed certificate", "A portfolio or GitHub showing real, working projects", "Years of experience only, with no project evidence"], "correct_index": 2, "explanation": "A visible portfolio or GitHub of working projects is commonly what junior mobile developer postings ask candidates to show."},
                {"question": "In the sample interview question about fetching and displaying API data, which combination of tools is the strongest answer built on?", "options": ["Only AsyncStorage, with no networking", "A single giant function with no state", "Alert.alert for all data display", "useEffect for fetching, useState for data/loading/error, and FlatList for rendering"], "correct_index": 3, "explanation": "This combination (useEffect, useState, FlatList, try/catch) is the standard, expected pattern for handling API-driven lists in React Native."},
                {"question": "What should a developer be ready to explain about each project in an interview, beyond 'it works'?", "options": ["What problem it solves and specific technical decisions made while building it", "Nothing more is needed", "Only the exact number of lines of code", "The exact date it was built"], "correct_index": 0, "explanation": "Interviewers value candidates who can articulate the problem solved and reasoning behind specific technical choices, not just working code."}
            ],
            "resources": []
        },
        {
            "day_number": 26,
            "week_number": 6,
            "week_title": "Capstone Preparation and Delivery",
            "title": "Planning Your Final Project: Scope, Screens, and Data Model",
            "learning_objective": "By the end of this class, you will be able to write a scoped project plan defining your final app's screens, data, and API integration.",
            "duration_minutes": 30,
            "content_html": """<p>The single biggest risk to finishing a portfolio project is scope: picking something too ambitious to finish, or too thin to be impressive. Today is entirely about planning your final project properly before writing any final project code, exactly as a professional would before starting client work.</p><h2>Choosing and Scoping Your Idea</h2><p>Pick one idea (a campus events tracker, a personal budget app, a study group finder, a local services directory) and write down: the app's core purpose in one sentence, its required screens (minimum four), what data it persists locally, and which real API it will call.</p><pre><code>App: Campus Study Group Finder
Purpose: Let students find and join study groups for their courses.
Screens: Home (list of groups), Group Detail, Create Group (form), Profile
Local persistence: Joined groups saved to AsyncStorage
API: Fetches course/subject data from a public API OR a mock JSON API
      you host yourself (e.g. via a free service)</code></pre><h2>Sketching Your Data Model</h2><p>Write out the shape of your core data object before coding. This single step prevents most mid-project restructuring.</p><pre><code>{
  id: "1",
  title: "Calculus II Study Group",
  course: "MTH201",
  meetingTime: "Tuesdays 5pm",
  members: ["Ada", "Tunde"]
}</code></pre><p>This plan is what you will execute starting Day 30, so treat today's output as a real spec, not a rough note.</p>""",
            "key_concepts": ["project scoping", "screen planning", "data modeling", "avoiding over/under-scoping"],
            "practical_exercise": {
                "title": "Write Your Final Project Spec",
                "instructions": "Write a one-page spec for your final project idea including: a one-sentence purpose, a list of at least four required screens, what data persists locally with AsyncStorage, which real API you will integrate, and a sample JSON object showing your core data model's shape. Submit this spec as your plan for the final project."
            },
            "quiz": [
                {"question": "Why is scoping a project properly before coding important?", "options": ["It wastes time better spent coding", "It reduces the risk of picking something too ambitious to finish or too thin to be impressive", "Scoping is only needed for team projects", "It has no effect on project outcomes"], "correct_index": 1, "explanation": "Proper scoping balances ambition and feasibility, reducing the risk of an unfinished or unimpressive final project."},
                {"question": "What is the benefit of sketching a data model's shape before writing code?", "options": ["It prevents most mid-project restructuring by clarifying the data early", "Data models are not needed in mobile apps", "It replaces the need for any screens", "It only matters for backend developers, not mobile"], "correct_index": 0, "explanation": "Defining the shape of core data objects upfront helps avoid major rework partway through building screens around that data."},
                {"question": "According to this lesson, what is the minimum number of distinct screens the final project should plan for?", "options": ["One", "Two", "Four", "Ten"], "correct_index": 2, "explanation": "The final project requires at least four distinct screens connected with real navigation."}
            ],
            "resources": []
        },
        {
            "day_number": 27,
            "week_number": 6,
            "week_title": "Capstone Preparation and Delivery",
            "title": "Choosing and Testing a Real API for Your Final Project",
            "learning_objective": "By the end of this class, you will be able to select, test, and integrate a suitable public API for your final project's live data requirement.",
            "duration_minutes": 25,
            "content_html": """<p>Your final project requires at least one real API integration, and choosing the wrong API, one that is unreliable, requires a paid key you cannot get, or does not fit your idea, can derail your last few days. Today is about locking this decision in safely, before Day 30.</p><h2>Evaluating an API Before Committing</h2><p>Before building around any API, test it directly: does it require authentication you can actually obtain for free, does it return data in a shape you can use, and is it currently online and responding.</p><pre><code>// Test any candidate API directly in a browser or with curl first:
// https://api.example.com/items
// Confirm: status 200, valid JSON, no confusing auth errors</code></pre><h2>A Reliable Fallback Strategy</h2><p>If your ideal API is unreliable or requires approval you cannot get in time, a free service like a simple hosted JSON API, or a public dataset API relevant to your idea, is a completely legitimate substitute. What matters for grading is a real network request to a real external endpoint, not which specific API you picked.</p><h2>Writing Your API Integration Plan</h2><p>Document exactly which endpoint(s) you will call, what data you expect back, and where in your app that data appears, so Day 30 begins with execution, not more research.</p>""",
            "key_concepts": ["API evaluation", "authentication requirements", "fallback API strategy", "integration planning"],
            "practical_exercise": {
                "title": "Confirm Your Final Project's API",
                "instructions": "Test your chosen API endpoint directly (in a browser or a tool like Postman/curl) and confirm it returns valid data with no blocking authentication issues. Write a short integration plan listing the exact endpoint(s), the data fields you will use, and which screen(s) will display them. Submit your test result (screenshot of the raw response) and your integration plan."
            },
            "quiz": [
                {"question": "Why should you test an API directly before building your app's integration around it?", "options": ["Testing is unnecessary and wastes time", "APIs never have authentication requirements", "It guarantees the API will never change", "To confirm it is online, returns usable data, and does not require unobtainable authentication"], "correct_index": 3, "explanation": "Verifying an API works and is accessible before building around it avoids wasted effort discovering problems late in the project."},
                {"question": "What matters most for the final project's API requirement, according to this lesson?", "options": ["Using the most famous API possible", "Making a real network request to a real external endpoint, regardless of which specific API", "The API must be a Nigerian company's API", "The API must require a paid subscription"], "correct_index": 1, "explanation": "The grading requirement is a genuine live API integration; the specific API chosen matters far less than that it is real and working."},
                {"question": "What should an API integration plan document before Day 30?", "options": ["Nothing, it can be figured out while building", "Only the app's color scheme", "The exact endpoints, expected data fields, and which screens will display them", "The developer's personal schedule"], "correct_index": 2, "explanation": "A clear integration plan (endpoints, data fields, target screens) lets final project work begin with execution rather than research."}
            ],
            "resources": [
                {"label": "Public APIs Directory", "url": "https://github.com/public-apis/public-apis"}
            ]
        },
        {
            "day_number": 28,
            "week_number": 6,
            "week_title": "Capstone Preparation and Delivery",
            "title": "Writing a README and Preparing Your Portfolio Presentation",
            "learning_objective": "By the end of this class, you will be able to write a professional README and plan a clear project demo.",
            "duration_minutes": 25,
            "content_html": """<p>A brilliant app with no README and a confusing demo can still fail to impress an employer, because they cannot quickly understand what they are looking at. How you present a project is part of the skill, not an afterthought.</p><h2>What a Strong README Includes</h2><pre><code># Campus Study Group Finder

A React Native app for finding and joining course study groups.

## Features
- Browse and search study groups by course
- Join a group (persisted locally)
- View group details and meeting times
- Live course data from [API name]

## Tech Stack
React Native, Expo, React Navigation, AsyncStorage

## Running Locally
npm install
npx expo start

## Screenshots
[add screenshots here]</code></pre><h2>Planning a Clear Demo</h2><p>A good demo video or live walkthrough follows a script: state the app's purpose in one sentence, show each core screen in order, demonstrate the API-driven feature and the persistence feature explicitly (close and reopen the app on camera), and mention one technical decision you are proud of. This is exactly what you will record on Day 30's follow-through.</p><p>Employers skim; a clear README and a 60-90 second demo often get more attention than the code itself on a first pass.</p>""",
            "key_concepts": ["README structure", "project documentation", "demo planning", "portfolio presentation"],
            "practical_exercise": {
                "title": "Write Your README and Demo Script",
                "instructions": "Write a complete README.md for an existing project (features, tech stack, setup instructions, and a placeholder for screenshots), and write a short demo script (5-8 bullet points) covering exactly what you will show and say in order for a 60-90 second walkthrough. Submit your README.md file and your demo script."
            },
            "quiz": [
                {"question": "Why does a project's README matter even if the code itself is strong?", "options": ["READMEs have no real impact on how a project is perceived", "READMEs are only required for open-source projects", "It helps reviewers quickly understand the project's purpose, features, and setup without reading all the code", "It replaces the need for the app to actually work"], "correct_index": 2, "explanation": "A clear README lets reviewers quickly grasp a project's purpose and structure, which matters since employers often skim rather than read every line of code."},
                {"question": "According to this lesson, what should a demo explicitly show for a project with local persistence?", "options": ["Nothing related to persistence needs to be shown", "Closing and reopening the app on camera to prove data survives a restart", "Only the app's loading screen", "The developer's code editor settings"], "correct_index": 1, "explanation": "Explicitly demonstrating an app closing and reopening with data intact proves the persistence feature actually works, not just that the code exists."},
                {"question": "What is a recommended length for a project demo walkthrough?", "options": ["10 seconds", "30 minutes", "There is no useful guideline", "60-90 seconds"], "correct_index": 3, "explanation": "A concise 60-90 second demo respects a reviewer's time while still covering the app's purpose and core features clearly."}
            ],
            "resources": [
                {"label": "GitHub: About READMEs", "url": "https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes"}
            ]
        },
        {
            "day_number": 29,
            "week_number": 6,
            "week_title": "Capstone Preparation and Delivery",
            "title": "Final Code Review: Cleaning Up Before You Ship",
            "learning_objective": "By the end of this class, you will be able to review and clean up an app's codebase for consistency, dead code, and crash risks before final submission.",
            "duration_minutes": 25,
            "content_html": """<p>The day before you build your final project is the right time to review your habits, not your final project itself, which does not exist yet. Today you do a real code review pass on a completed earlier app, catching the kind of issues that make experienced developers wince and give you a checklist to apply again on Day 30's build.</p><h2>A Practical Pre-Ship Checklist</h2><ul><li>Remove leftover <code>console.log</code> debug statements</li><li>Delete unused components, imports, and commented-out code blocks</li><li>Confirm every list has a proper unique <code>keyExtractor</code>, not array index</li><li>Confirm every screen handles loading, error, and empty states, not just the happy path</li><li>Confirm destructive actions have a confirmation step</li><li>Rename any placeholder variables like <code>data2</code> or <code>temp</code> to descriptive names</li></ul><h2>Why This Habit Matters</h2><p>Code review is a normal part of every professional engineering job; pull requests get rejected for exactly these kinds of issues. Practicing self-review now, catching your own sloppy patterns before anyone else has to, is a skill that compounds across your whole career, and it is what you will apply to your final project as you build it tomorrow and beyond.</p>""",
            "key_concepts": ["code review checklist", "removing dead code", "crash-risk patterns", "self-review habits"],
            "practical_exercise": {
                "title": "Run a Self Code Review",
                "instructions": "Pick one earlier project and go through the full pre-ship checklist against it: remove console.logs and dead code, fix any keyExtractor using array index, confirm loading/error/empty states exist, and confirm destructive actions have confirmations. Submit a short before/after list of every specific issue you found and fixed."
            },
            "quiz": [
                {"question": "Why should leftover console.log statements be removed before considering code finished?", "options": ["They cause the app to crash", "They are debug artifacts that clutter production-quality code and can leak internal data", "console.log is not allowed by React Native at all", "They make the app run faster"], "correct_index": 1, "explanation": "Leftover console.log calls are debug clutter in finished code and can unintentionally expose internal data or state."},
                {"question": "What should be confirmed about every screen's list before shipping?", "options": ["That it has a unique keyExtractor, not array index", "That it contains at least 100 items", "That it uses only red color styling", "Nothing, lists do not need review"], "correct_index": 0, "explanation": "A proper unique keyExtractor (not array index) prevents subtle rendering bugs when list items are added, removed, or reordered."},
                {"question": "Why is practicing self-code-review considered valuable for a career, beyond this one project?", "options": ["It has no long-term value", "Code review is a normal, ongoing part of professional engineering jobs, and self-review catches issues early", "Only senior developers ever need to review code", "It replaces the need for testing entirely"], "correct_index": 1, "explanation": "Code review is standard in real engineering teams, and developing the habit of self-review early builds a skill that compounds over a career."}
            ],
            "resources": []
        },
        {
            "day_number": 30,
            "week_number": 6,
            "week_title": "Capstone Preparation and Delivery",
            "title": "Building and Demoing Your Multi-Screen Mobile App",
            "learning_objective": "By the end of this class, you will be able to execute your planned final project into a working, demoable multi-screen mobile app.",
            "duration_minutes": 40,
            "content_html": """<p>Today you execute the plan you built over the last several days into your final project: <strong>Build and Demo a Multi-Screen Mobile App</strong>. This is the single deliverable that proves everything you learned across this track, and it should look and feel like a real app, not a tutorial exercise.</p><h2>Executing Against Your Spec</h2><p>Return to your Day 26 spec (screens, data model) and your Day 27 API integration plan, and start building using the exact patterns practiced across this track: a Stack and/or Tab navigator for your four-plus screens, AsyncStorage for local persistence, a fetch-based service layer for your real API, loading/error/empty states on every data-driven screen, and your theme file from Day 16 applied consistently.</p><pre><code>my-final-app/
  screens/        // Home, Detail, Create/Form, Profile (minimum 4)
  components/
  context/        // shared state if needed
  services/api.js // your real API integration
  theme.js
  App.js</code></pre><h2>Building Toward the Demo</h2><p>As you build, keep your Day 28 demo script in mind: after each core feature works, test it exactly as you plan to demo it, including closing and reopening the app to confirm persistence and testing the API screen with the network briefly toggled off to confirm your error state is real, not just theoretical.</p><p>By the end of today, or shortly after, you should have a working app on your phone, a demo recording following your script, and a README describing it, ready to add directly to your portfolio.</p>""",
            "key_concepts": ["final project execution", "applying the full stack learned", "demo-driven testing", "portfolio delivery"],
            "practical_exercise": {
                "title": "Start and Build Your Final Project: Build and Demo a Multi-Screen Mobile App",
                "instructions": "This IS the start of your final project. Using your Day 26 spec and Day 27 API plan, begin building your final project app now: set up navigation for at least four screens, wire up AsyncStorage persistence, integrate your chosen real API with loading/error/empty states, and apply your theme consistently. Submit your in-progress or completed project code, and once finished, a demo recording following your Day 28 script plus your README."
            },
            "quiz": [
                {"question": "What is the minimum number of distinct, navigable screens the final project requires?", "options": ["Two", "Three", "Four", "Eight"], "correct_index": 2, "explanation": "The final project brief requires at least four distinct screens connected with real navigation."},
                {"question": "Why should you test the API-driven screen with the network briefly toggled off during final project work?", "options": ["To make the app crash intentionally", "To confirm the error state actually works and is not just theoretical", "Turning off the network is required by app stores", "There is no reason to do this"], "correct_index": 1, "explanation": "Manually triggering a network failure verifies that error handling genuinely works, rather than only being tested against the happy path."},
                {"question": "According to today's lesson, what three artifacts should exist by the time the final project is complete?", "options": ["Only the source code", "The working app, a demo recording, and a README", "A PowerPoint presentation only", "A printed manual"], "correct_index": 1, "explanation": "The final deliverable set is the working app on a device, a demo recording following the planned script, and a documenting README."}
            ],
            "resources": [
                {"label": "React Navigation Documentation", "url": "https://reactnavigation.org/docs/getting-started"},
                {"label": "Expo Documentation", "url": "https://docs.expo.dev/"}
            ]
        }
    ]
}
