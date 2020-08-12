<template>
  <div id="wrapper">
    <header>
      <span class="title">Bybit Position Calculator</span>
    </header>
    <main>
      <div class="left-column">
        <inverse></inverse>
      </div>
      <div class="right-column">
        <usdt></usdt>
      </div>
    </main>
  </div>
</template>

<script>
import Inverse from './Inverse/Inverse.vue';
import Usdt from './Usdt/Usdt.vue';

export default {
  name: 'landing-page',
  components: { Inverse, Usdt }
};
</script>

<style>
/* @import url('https://fonts.googleapis.com/css?family=Source+Sans+Pro'); */

:root {
  --body-bg-color: #101014;
  --main-box-shadow: 0px 0px 2px 1px rgba(0, 0, 0, 0.3);
  --main-bg-color: #18191F;
  --color-green: #00C195;
  --color-red: #F94C4C;
  --color-alt: rgba(255, 255, 255, 0.25);
  --color-alt-1: rgba(255, 255, 255, 0.5);
  --color-alt-2: rgba(255, 255, 255, 0.75);
}

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
  color: #fff;
}

header {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-color: var(--main-bg-color);
  /* padding: 10px 20px 10px 20px; */
  font-weight: 700;
  padding: 0.5rem 1rem;
}

header .title {
  font-size: 35px;
}

body {
  font-family: 'Source Sans Pro', sans-serif;
  background-color: var(--body-bg-color);
  font-size: 14px;
  color: rgba(255, 255, 255, 0.87);
  display: grid;
  height: 100vh;
  grid-template-rows: auto 1fr auto;
}

main {
  display: grid;
  grid-template-columns: auto auto;
  height: 100%;
  width: 100%;
  padding: 10px;
}
div.right-column {
  width: 100%;
}
div.left-column {
  width: 100%;
}

footer {
  padding: 0.5rem 1rem;
  background: var(--main-bg-color);
}

div.panel {
  margin: 5px;
  background: var(--main-bg-color);
  border-radius: 5px;
  padding: 5px;
}
div.panel > div.title {
  width: 100%;
  font-size: 16px;
  font-weight: 700;
  border-bottom: 1px solid var(--color-alt);
  padding: 0.5rem;
}

table {
  background-color: var(--main-bg-color);
  /* padding: 10px; */
  /* border-radius: 5px; */
  width: 100%;
}
table.bordered  {
  border: 1px solid var(--color-alt);
}
tr, th, td {
  padding: 5px;
}
td.number, th.number {
  text-align: right;
}
th.title {
  font-size: 16px;
  font-weight: 700;
  border-bottom: 1px solid var(--color-alt);
}
tr.underline > th {
  border-bottom: 1px solid var(--color-alt);
}

select {
  background-color: transparent;
  border: 1px solid var(--color-alt);
  padding: 5px;
  border-radius: 5px;
  line-height: 200%;
}

select:hover {
  background-color: rgba(255, 255, 255, 0.08);
}

option {
  background-color: #212121;
}

input {
  background-color: transparent;
  border: 1px solid rgba(255, 255, 255, 0.25);
  border-radius: 5px;
  padding: 5px 10px 5px 10px;
}

input.number {
  font-family: 'Fira Mono', monospace;
}

input.green {
  background-color: var(--color-green);
  border-color: transparent;
}
input.red {
  background-color: var(--color-red);
  border-color: transparent;
}

input:hover {
  border: 1px solid var(--color-alt-2);
}

.color-green {
  color: var(--color-green)
}
.color-red {
  color: var(--color-red)
}

.header-top {
  margin-bottom: 10px;
}

.welcome {
  color: #555;
  font-size: 23px;
  margin-bottom: 10px;
}

.title.alt {
  font-size: 18px;
  margin-bottom: 10px;
}

.doc p {
  color: black;
  margin-bottom: 10px;
}

.doc button {
  font-size: .8em;
  cursor: pointer;
  outline: none;
  padding: 0.75em 2em;
  border-radius: 2em;
  display: inline-block;
  color: #fff;
  background-color: #4fc08d;
  transition: all 0.15s ease;
  box-sizing: border-box;
  border: 1px solid #4fc08d;
}

.doc button.alt {
  color: #42b983;
  background-color: transparent;
}
</style>
