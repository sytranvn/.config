return {
  'akinsho/bufferline.nvim',
  version = "*",
  dependencies = 'nvim-tree/nvim-web-devicons',
  config = function()
    local nmap = function(keys, func, desc)
      if desc then
        desc = 'Buffer: ' .. desc
      end

      vim.keymap.set('n', keys, func, { desc = desc })
    end


    require('bufferline').setup {
      options = {
        buffer_close_icon = '󰅖',
        modified_icon = '●',
        close_icon = '',
      }
    }
    nmap('<C-c>', function()
        if require('bufferline.utils').get_buf_count() > 1 then
          require('bufferline.commands').cycle(1)
          vim.cmd("bd #")
        else
          vim.cmd("bd")
        end
      end,
      "Close current buffer"
    )
    nmap('gn', function() require('bufferline').cycle(1) end, "Next buffer")
    nmap('gp', function() require('bufferline').cycle(-1) end, "Previous buffer")
    vim.api.nvim_create_user_command('BufferLineCloseOthers', function()
      vim.cmd('BufferLineCloseLeft')
      vim.cmd('BufferLineCloseRight')
    end, {})
  end
}
