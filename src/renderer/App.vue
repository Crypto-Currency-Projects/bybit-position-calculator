<template>
  <v-app>
    <div id="header">
      <v-app-bar
      color="primary"
      dense
      dark
      >
        <v-toolbar-title>Bybit Position Calculator</v-toolbar-title>
      </v-app-bar>
    </div>
    <v-main>
      <notifications group="main" />
      <position-calculator></position-calculator>
    </v-main>
  </v-app>
</template>

<script>
import positionCalculator from './components/PositionCalculator'

export default {
  name: 'bybit-position-calculator',
  components: { positionCalculator }
}
</script>

<style lang="scss">
/* :root {
  --body-bg-color: #101014;
  --main-box-shadow: 0px 0px 2px 1px rgba(0, 0, 0, 0.3);
  --main-bg-color: #18191F;
  --color-green: #00C195;
  --color-red: #F94C4C;
  --color-outline: rgba(255, 255, 255, 0.25);
  --color-outline-1: rgba(255, 255, 255, 0.5);
  --color-outline-2: rgba(255, 255, 255, 0.75);
  --color-highlight: rgba(255, 255, 255, 0.08);
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
  display: grid;
  grid-template-rows: auto 1fr auto;
}

main {
  display: grid;
  grid-template-columns: 50% 50%;
  height: 100%;
  width: 100%;
  padding: 10px;
  > .grid-column {
    width: 100%;
    .panel {
      margin: 5px;
      background: var(--main-bg-color);
      border-radius: 5px;
      > div.header {
        width: 100%;
        font-size: 16px;
        font-weight: 700;
        border-bottom: 1px solid var(--color-outline);
        padding: 0.5rem;
        align-items: center;
      }
      > div.body {
        padding: 0.5rem;
      }
    }
  }
}

footer {
  padding: 0.5rem 1rem;
  background: var(--main-bg-color);
}

table {
  background-color: var(--main-bg-color);
  width: 100%;
  tr, th, td {
    padding: 5px;
  }
  th.title {
    font-size: 16px;
    font-weight: 700;
    border-bottom: 1px solid var(--color-outline);
  }
  tr.header > th {
    border-bottom: 1px solid var(--color-outline);
  }
  th, td {
    &.number {
      text-align: right;
    }
  }
  &.bordered {
    border: 1px solid var(--color-outline)
  }
}

select {
  background-color: transparent;
  border: 1px solid transparent;
  border-bottom: 1px solid var(--color-outline);
  padding: 5px;
  // border-radius: 5px;
  line-height: 200%;
}

select:hover {
  background-color: var(--color-highlight)
}

option {
  background-color: #212121;
}

input {
  background-color: transparent;
  border: 1px solid var(--color-outline);
  border-radius: 5px;
  box-shadow: 0px 0px 2px 1px rgba(0, 0, 0, 0.3);
  padding: 5px 10px 5px 10px;
  &.number {
    font-family: 'Fira Mono', monospace;
  }
  &.filled {
    background-color: #5767FF;
    border-color: transparent;
  }
  &.filled-green {
    background-color: var(--color-green);
    border-color: transparent;
  }
  &.filled-red {
    background-color: var(--color-red);
    border-color: transparent;
  }
}

input:hover {
  border: 1px solid var(--color-outline-2)
}

.bold {
  font-weight: 700;
}

.color-green {
  color: var(--color-green)
}
.color-red {
  color: var(--color-red)
}*/
</style>
