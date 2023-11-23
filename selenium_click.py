

def element_click(driver, element):
    driver.execute_script('arguments[0].scrollIntoView({behavior: "smooth", block: "center"});', element)
    driver.execute_script('arguments[0].click();', element)
