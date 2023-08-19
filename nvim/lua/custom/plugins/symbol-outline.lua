return {
  'simrat39/symbols-outline.nvim',
  config = function()
    require('symbols-outline').setup()
    vim.api.nvim_set_keymap('n', '<leader>so', ':SymbolsOutline<CR>', { desc = '[S]ymbol [O]utline' })
  end
}
