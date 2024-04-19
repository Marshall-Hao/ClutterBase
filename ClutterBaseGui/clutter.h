#ifndef CLUTTER_H
#define CLUTTER_H

#include <QDialog>

namespace Ui {
class Clutter;
}

class Clutter : public QDialog
{
    Q_OBJECT

public:
    explicit Clutter(QWidget *parent = nullptr);
    ~Clutter();

private:
    Ui::Clutter *ui;
};

#endif // CLUTTER_H
