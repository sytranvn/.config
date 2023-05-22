return {
  'echasnovski/mini.nvim',
  version = '*',
  config = function()
    require('mini.surround').setup {}
    require('mini.comment').setup {}
    require('mini.pairs').setup {}
    require('mini.map').setup {}
  end
}
-- vim: ts=2 sts=2 sw=2 etm
