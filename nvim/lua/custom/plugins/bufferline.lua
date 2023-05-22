return {
  'akinsho/bufferline.nvim',
  version = "*",
  dependencies = 'nvim-tree/nvim-web-devicons',
  config = function()
    require('bufferline').setup {}
    vim.keymap.set('n', '<C-c>', function()
      require('bufferline.commands').cycle(1)
      vim.cmd("bd #")
    end, { desc = "Close current buffer" })
  end
}
