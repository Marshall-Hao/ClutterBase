#include "clutter.h"
#include "ui_clutter.h"

Clutter::Clutter(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::Clutter)
{
    ui->setupUi(this);
}

Clutter::~Clutter()
{
    delete ui;
}
