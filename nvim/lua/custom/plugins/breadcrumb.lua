return {
  "loctvl842/breadcrumb.nvim",
  config = function()
    require("breadcrumb").setup({
      disabled_filetype = {
        "",
        "help",
      },
      icons = {
        File = " ",
        Module = " ",
        Namespace = " ",
        Package = " ",
        Class = " ",
        Method = " ",
        Property = " ",
        Field = " ",
        Constructor = "",
        Enum = " ",
        Function = "󰊕 ",
        Variable = " ",
        Constant = " ",
        String = " ",
        Number = " ",
        Boolean = " ",
        Array = " ",
        Object = "{}",
        Key = " ",
        Null = "󰟢 ",
        EnumMember = " ",
        Struct = "{} ",
        Event = " ",
        Operator = " ",
        TypeParameter = " ",
      },
      separator = ">",
      depth_limit = 0,
      depth_limit_indicator = "..",
      color_icons = true,
      highlight_group = {
        component = "BreadcrumbText",
        separator = "BreadcrumbSeparator",
      },
    })
  end
}
