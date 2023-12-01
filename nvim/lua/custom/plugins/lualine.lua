return {
  -- Set lualine as statusline
  'nvim-lualine/lualine.nvim',
  dependencies = {
    "loctvl842/breadcrumb.nvim"
  },
  -- See `:help lualine.txt`
  config = function()
    local breadcrumb = function()
      local breadcrumb_status_ok, breadcrumb = pcall(require, "breadcrumb")
      if not breadcrumb_status_ok then
        return
      end
      return breadcrumb.get_breadcrumb()
    end

    require('lualine').setup({
      options = {
        icons_enabled = true,
        theme = 'tokyonight',
        component_separators = '|',
        section_separators = '',
      },
      sections = {
        lualine_y = {
          'progress',
          'location'
        },
        lualine_z = {
          {
            'datetime',
            -- options: default, us, uk, iso, or your own format string ("%H:%M", etc..)
            style = "%H:%M"
          },
        }
      },
      winbar = {
        lualine_c = { breadcrumb },
      },
      inactive_winbar = {
      },
      tabline = {
        lualine_a = { 'filename' },
        lualine_b = {},
        lualine_c = {},
        lualine_x = {},
        lualine_y = {},
        lualine_z = {}
      }
    })
    vim.api.nvim_create_user_command("BuffCloseOthers", function()
      local bufs = vim.api.nvim_list_bufs()
      local current_buf = vim.api.nvim_get_current_buf()
      for _, i in ipairs(bufs) do
        if i ~= current_buf then
          if vim.api.nvim_buf_get_option(i, "modified") then
            vim.api.nvim_echo({ { "Unsaved file " .. vim.api.nvim_buf_get_name(i), "WarningMsg" } }, false, {})
          else
            vim.api.nvim_buf_delete(i, {})
          end
        end
      end
    end, {})

    vim.keymap.set('n', 'gn', ':bn<CR>', { silent = true })
    vim.keymap.set('n', 'gN', ':bp<CR>', { silent = true })
  end
}
