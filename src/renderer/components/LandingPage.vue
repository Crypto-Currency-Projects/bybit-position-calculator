<template>
  <div id="wrapper">
    <body>
      <!-- <img id="logo" src="~@/assets/logo.png" alt="electron-vue"> -->
      <header>
        <span class="title">Bybit Position Calculator</span>
      </header>
      <main>
        <h1>Inverse Contract</h1>
        <position-calculator></position-calculator>
      </main>
    </body>
  </div>
</template>

<script>
  import SystemInformation from './LandingPage/SystemInformation'
  import PositionCalculator from './PositionCalculator/PositionCalculator'

  export default {
    name: 'landing-page',
    components: { SystemInformation, PositionCalculator },
    methods: {
      open (link) {
        this.$electron.shell.openExternal(link)
      }
    }
  }
</script>

<style>
  @import url('https://fonts.googleapis.com/css?family=Source+Sans+Pro');
  /* https://colorhunt.co/palette/69360 */

  * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
    color: #fff;
  }

  header {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: #18181B;
    padding: 10px 20px 10px 20px;
  }

  header .title {
    font-size: 35px;
    font-weight: bold;
  }

  body {
    font-family: 'Source Sans Pro', sans-serif;
    color: rgba(255, 255, 255, 0.87);
    background-color: #0E0E10;
  }

  main {
    /* background:
      radial-gradient(
        ellipse at top left,
        rgba(255, 255, 255, 1) 40%,
        rgba(229, 229, 229, .9) 100%
      ); */
    height: 100%;
    width: 100%;
    padding: 60px 80px;
    align-items: center;
    align-content: center;
  }

  #logo {
    height: auto;
    margin-bottom: 20px;
    width: 420px;
  }

  main {
    /*display: flex;*/
    justify-content: center;
  }

  table {
    background-color: #18181B;
    border: 2px transparent;
    border-radius: 5px;
    box-shadow: 0px 0px 3px 2px rgba(0, 0, 0, 0.3);
    width: auto;
  }
  tr, th, td {
    padding: 10px;
  }

  select {
    background-color: transparent;
    border: 1px solid rgba(255, 255, 255, 0.25);
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

  td th.number {
    text-align: right;
    font-family: 'Fira Mono', monospace;
  }

  input {
    background-color: transparent;
    border: 0px;
    border: 1px solid rgba(255, 255, 255, 0.25);
    border-radius: 5px;
    padding: 5px 10px 5px 10px;
  }

  input.number {
    font-family: 'Fira Mono', monospace;
  }

  input:hover {
    border: 1px solid rgba(255, 255, 255, 0.75)
  }


  button {
    background-color: transparent;
    padding: 5px;
    border: 1px solid rgba(255, 255, 255, 0.75);
    border-radius: 5px;
    font-weight: bold;
  }

  button.blue {
    background-color: #6574FF;
  }

  button:hover {
    background-color: rgba(255, 255, 255, 0.08);
  }

  main > div { flex-basis: 50%; }

  .left-side {
    display: flex;
    flex-direction: column;
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
