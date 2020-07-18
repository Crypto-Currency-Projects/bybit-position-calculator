<template>
  <div class="container">
    <input
      class="todo-input"
      type="text" v-model="todoItemName"
      placeholder="What are you doing today?" @keyup.enter.prevent="addTODO"
    >
    <div class="todos">
      <ul>
        <li v-for="todo in todos"
        :key="todo.id">{{todo.name}}</li>
      </ul>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  data () {
    return {
      todoItemName: ''
    }
  },
  methods: {
    addTodo () {
      this.$store.dispatch('ADD_TODO', this.todoItemName)
      this.todoItemName = ''
    }
  },
  computed: {
    ...mapState({
      todos: state => state.Todo.todos
    })
  }
}
</script>

<style>
.todo-input {
  font-family: 'Fira Mono Medium', Fira Mono, monospace;
  background-color: #1E1E1E;
  color: #FFFFFF;
  padding: 5px;
  padding-left: 10px;
  padding-right: 10px;
  width: auto;
  border: 2px solid rgba(255, 255, 255, 0.2);
  border-radius: 5px;
  box-shadow: 0px 0px 2px 1px rgba(0, 0, 0, 0.3);
}
</style>