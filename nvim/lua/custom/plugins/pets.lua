return {
  "giusgad/pets.nvim",
  version = "*",
  dependencies = {
    "MunifTanjim/nui.nvim", "giusgad/hologram.nvim"
  },
  event = "VeryLazy",
  config = function()
    require('pets').setup {
      default_pet = "dog",
      death_animation = true,
      random = true,
      row = 1,
      col = 0,
    }
  end,
}
-- vim: ts=2 sts=2 sw=2 et
