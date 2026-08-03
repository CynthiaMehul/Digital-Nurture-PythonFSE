# API Integration & Advanced State Management

## State Management Comparison

### React + Redux Toolkit

React does not include a built-in global state management system. Redux Toolkit is used to manage shared application state.

Redux Toolkit uses:

- Store
- Slices
- Actions
- Reducers
- Selectors
- Async Thunks

`createAsyncThunk()` handles asynchronous operations such as API calls. Redux Toolkit reduces much of the boilerplate required by traditional Redux.

Learning curve: Moderate

Boilerplate: Moderate

Built-in tooling: React DevTools and Redux DevTools

---

### Angular + NgRx

NgRx follows the Redux architecture and is designed for Angular applications.

NgRx uses:

- Actions
- Reducers
- Selectors
- Effects
- Store

Effects handle side effects such as API calls. Reducers remain pure and only update state.

Data flow:

Component → Action → Effect → API → Reducer → State → Selector → Component

Learning curve: High

Boilerplate: High

Built-in tooling: Angular DevTools and NgRx Store DevTools

---

### Vue + Pinia

Pinia is the recommended state management library for Vue.

Pinia uses:

- Stores
- State
- Getters
- Actions

Pinia actions can handle both synchronous state updates and asynchronous API calls. Pinia has less boilerplate than Redux and NgRx.

`storeToRefs()` is used to extract reactive state from a Pinia store without losing reactivity.

Learning curve: Low to Moderate

Boilerplate: Low

Built-in tooling: Vue DevTools and Pinia DevTools

---

## Summary

| Feature | React + Redux Toolkit | Angular + NgRx | Vue + Pinia |
|---|---|---|---|
| State management | External library | External library | Official recommended library |
| Boilerplate | Moderate | High | Low |
| Learning curve | Moderate | High | Low to Moderate |
| Async API handling | Async Thunks | Effects | Async Actions |
| State access | Selectors | Selectors | Store state and getters |
| DevTools | Redux DevTools | NgRx DevTools | Vue DevTools |
| Best suited for | Large React applications | Large Angular applications | Vue applications with simple, clean stores |