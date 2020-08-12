<template>
  <div class="panel" id="container">
    <div class="title">
      <span>Inverse Contract</span>
    </div>
    <table>
      <tr>
        <td>Ticker / Side</td>
        <td>
          <span>
            <select v-model="symbol">
              <option value="" disabled hidden>Select Ticker</option>
              <option>BTCUSD</option>
              <option>ETHUSD</option>
              <option>XRPUSD</option>
              <option>EOSUSD</option>
            </select>
          </span>
          <span>
            <select v-model="side">
              <option value="" disabled hidden>Side</option>
              <option>LONG</option>
              <option>SHORT</option>
            </select>
          </span>
        </td>
      </tr>
      <tr>
        <td>Account Balance (USD)</td>
        <td><input class="number" type="number" v-model.number="balance"></td>
      </tr>
      <tr>
        <td>Risk (%)</td>
        <td><input class="number" type="number" v-model.number="risk"></td>
      </tr>
      <tr>
        <td>Start Price</td>
        <td><input class="number" type="number" v-model.number="start"></td>
      </tr>
      <tr>
        <td>End Price</td>
        <td><input class="number" type="number" v-model.number="end"></td>
      </tr>
      <tr>
        <td>Stop Loss Price</td>
        <td><input class="number" type="number" v-model.number="stop"></td>
      </tr>
      <tr>
        <td>Number of Orders</td>
        <td><input class="number" type="number" v-model.number="orders"></td>
      </tr>
      <tr>
        <td></td>
        <td>
          <input type="button" @click="calculatePosition()" value="Submit">
        </td>
      </tr>
    </table>
    <table class="bordered">
      <tr><th class="title" colspan="2">Position Information</th></tr>
      <tr>
        <td colspan="2">
          <table class="bordered">
            <tr class="underline">
              <th>#</th>
              <th class="number">Price</th>
              <th class="number">Qty</th>
            </tr>
            <tr v-for="(order, num) in out['orders']">
              <td>{{ num + 1 }}</td>
              <td class="number">{{ order.price }}</td>
              <td class="number">{{ order.qty }}</td>
            </tr>
          </table>
        </td>
      </tr>
      <tr>
        <td>Maximum Leverage</td>
        <td class="number">{{ out["leverage"] }}x</td>
      </tr>
      <tr>
        <td>Total Contracts</td>
        <td class="number">{{ out["totalContracts"] }}</td>
      </tr>
      <tr>
        <td>Average Entry Price</td>
        <td class="number">{{ out["averagePrice"] }}</td>
      </tr>
    </table>
  </div>
</template>

<script src="./Inverse.js"></script>

<style>

</style>
